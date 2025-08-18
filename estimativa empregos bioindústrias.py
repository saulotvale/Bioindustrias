import pandas as pd
import numpy as np

# ---------------- Carregar base ----------------
arquivo = "Base 2.3 junho 2025.xlsx"
df = pd.read_excel(arquivo)

# Garantir tipos numéricos
df["capital"] = pd.to_numeric(df["capital"], errors="coerce").fillna(0)

# Normalizar categorias de porte
df["porte"] = df["porte"].replace({
    "Microempresa": "Microempresa",
    "Empresa de Pequeno Porte": "Empresa de Pequeno Porte",
    "Demais": "Demais"
})

# Definir limites e quantis por porte
valores_quantil = {
    "Microempresa": [2, 5, 10, 20],
    "Empresa de Pequeno Porte": [10, 20, 40, 100],
    "Demais": [50, 100, 200, 300],
}
minimos_porte = {"Microempresa":2, "Empresa de Pequeno Porte":10, "Demais":50}

# Inicializar coluna de empregos
df["empregos_diretos"] = np.nan

# ---- 1) MEI: 2 fixo ----
mask_mei = df["mei"] == "S"
df.loc[mask_mei, "empregos_diretos"] = 2

# ---- 2) Capital 0 -> mínimo do porte (exceto MEI) ----
mask_cap0 = (df["capital"]==0) & (~mask_mei)
df.loc[mask_cap0, "empregos_diretos"] = df.loc[mask_cap0, "porte"].map(minimos_porte)

# ---- 3) Associações privadas: mínimo 10, máximo 20 ----
mask_assoc = df["natjjud_extenso"]=="Associação Privada"
df.loc[mask_assoc, "empregos_diretos"] = df.loc[mask_assoc, "empregos_diretos"].fillna(0).clip(lower=10, upper=20)

# ---- 4) Quantis por UF e porte (não-MEI, não-associação, capital>0) ----
for uf in df["uf"].dropna().unique():
    for porte in ["Microempresa","Empresa de Pequeno Porte","Demais"]:
        mask = (
            (df["uf"]==uf) &
            (df["porte"]==porte) &
            (~mask_mei) &
            (~mask_assoc) &
            (df["capital"]>0)
        )
        sub = df.loc[mask]
        if sub.empty:
            continue
        q1 = sub["capital"].quantile(0.25)
        q2 = sub["capital"].quantile(0.50)
        q3 = sub["capital"].quantile(0.75)
        vals = valores_quantil[porte]
        caps = sub["capital"]
        df.loc[mask, "empregos_diretos"] = np.select(
            [caps<=q1, (caps>q1)&(caps<=q2), (caps>q2)&(caps<=q3), caps>q3],
            vals
        )

# ---- 5) Cooperativas: mínimo 20 para Micro e EPP ----
mask_coop = (df["natjjud_extenso"]=="Cooperativa") & (df["porte"].isin(["Microempresa","Empresa de Pequeno Porte"]))
df.loc[mask_coop, "empregos_diretos"] = df.loc[mask_coop, "empregos_diretos"].fillna(0).clip(lower=20)

# ---- 6) Filiais: pelo menos mínimo do porte ----
mask_filial = df["matriz_filial"]==2
df.loc[mask_filial & (~mask_mei), "empregos_diretos"] = df.loc[mask_filial & (~mask_mei), "empregos_diretos"].fillna(0)
df.loc[mask_filial, "empregos_diretos"] = df.loc[mask_filial, "empregos_diretos"].combine(
    df["porte"].map(minimos_porte),
    func=lambda x,y: max(x,y)
)

# ---- 7) Preencher NaN restantes com 0 ----
df["empregos_diretos"] = df["empregos_diretos"].fillna(0).astype(int)

# ---- 8) Blindagem final de limites ----
# Micro
mask_micro = (df["porte"]=="Microempresa") & ~mask_mei & ~mask_assoc
df.loc[mask_micro & (~df["empregos_diretos"].isin([2,5,10,20])), "empregos_diretos"]=10
# EPP
mask_epp = (df["porte"]=="Empresa de Pequeno Porte") & ~mask_assoc
df.loc[mask_epp & (~df["empregos_diretos"].isin([10,20,40,100])), "empregos_diretos"]=20
# Demais
mask_demais = (df["porte"]=="Demais") & ~mask_assoc
df.loc[mask_demais & (~df["empregos_diretos"].isin([50,100,200,300])), "empregos_diretos"]=50
# Associações privadas
df.loc[mask_assoc, "empregos_diretos"] = df.loc[mask_assoc, "empregos_diretos"].clip(lower=10, upper=20)

# ---- 9) Empregos indiretos ----
df["empregos_indiretos"] = df["empregos_diretos"] * 4

# ---- 10) Exportar ----
df.to_excel("Resultado_empregos_detalhado_final.xlsx", index=False)
resultado = df.groupby(["cod7_ibge","munic_extenso","uf"], as_index=False).agg(
    empregos_diretos=("empregos_diretos","sum"),
    empregos_indiretos=("empregos_indiretos","sum")
)
resultado.to_excel("Resultado_empregos_por_municipio_final.xlsx", index=False)

# ---- 11) Checagens rápidas ----
print("Resumo checagem de limites (diretos):")
print("Micro fora do conjunto {2,5,10,20}:",
      int(((df["porte"]=="Microempresa") & (~df["empregos_diretos"].isin([2,5,10,20]))).sum()))
print("EPP fora do conjunto {10,20,40,100}:",
      int(((df["porte"]=="Empresa de Pequeno Porte") & (~df["empregos_diretos"].isin([10,20,40,100]))).sum()))
print("Demais fora do conjunto {50,100,200,300}:",
      int(((df["porte"]=="Demais") & (~df["empregos_diretos"].isin([50,100,200,300]))).sum()))
print("Associações fora do conjunto {10-20}:",
      int(((df["natjjud_extenso"]=="Associação Privada") & ((df["empregos_diretos"]<10)|(df["empregos_diretos"]>20))).sum()))
print("Arquivos gerados com sucesso!")
