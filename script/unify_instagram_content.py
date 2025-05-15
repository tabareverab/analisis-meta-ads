# unify_instagram_content.py
# Author: Tabaré Vera Bordagaray
# Description:
# This script merges two CSV reports exported from Meta (Instagram): one for feed posts and one for stories.
# It aligns column structures, standardizes date and time fields, adds content origin tags,
# and generates a unified Excel file ready for further analysis.

# Requirements:
# - Run on Google Colab
# - Files must be uploaded in .csv format

# Outputs:
# - Contenido_Instagram_Unificado.xlsx

import pandas as pd
from google.colab import files
from datetime import datetime

# Upload files
print("📁 Upload the POSTS file first:")
uploaded_publicaciones = files.upload()

print("\n📁 Now upload the STORIES file:")
uploaded_historias = files.upload()

# Load files
df_pub = pd.read_csv(list(uploaded_publicaciones.keys())[0])
df_hist = pd.read_csv(list(uploaded_historias.keys())[0])

# Target column structure
columnas_objetivo = [
    'Identificador de la publicación', 'Identificador de la cuenta', 'Nombre de usuario de la cuenta',
    'Nombre de la cuenta', 'Descripción', 'Duración (segundos)', 'Hora de publicación',
    'Enlace permanente', 'Tipo de publicación', 'Comentario sobre los datos', 'Fecha',
    'Visualizaciones', 'Alcance', 'Me gusta', 'Veces que se compartió', 'Comentarios',
    'Veces que se guardó', 'Visitas al perfil', 'Respuestas', 'Toques en stickers', 'Navegación'
]

# Ensure all necessary columns exist
for col in columnas_objetivo:
    if col not in df_pub.columns:
        df_pub[col] = None
    if col not in df_hist.columns:
        df_hist[col] = None

# Process date and time
def procesar_fecha_hora(df):
    df = df.copy()
    df['Hora de publicación'] = pd.to_datetime(df['Hora de publicación'], errors='coerce')
    df['Fecha'] = df['Hora de publicación'].dt.strftime('%d-%m-%Y')
    df['Hora de publicación'] = df['Hora de publicación'].dt.strftime('%H:%M')
    return df

df_pub = procesar_fecha_hora(df_pub)
df_hist = procesar_fecha_hora(df_hist)

# Add source column and align
df_pub = df_pub[columnas_objetivo]
df_pub["Origen"] = "Publicación"

df_hist = df_hist[columnas_objetivo]
df_hist["Origen"] = "Historia"

# Merge both
df_final = pd.concat([df_pub, df_hist], ignore_index=True)

# Save to Excel
output_filename = "Contenido_Instagram_Unificado.xlsx"
df_final.to_excel(output_filename, index=False)

# Trigger download
files.download(output_filename)
