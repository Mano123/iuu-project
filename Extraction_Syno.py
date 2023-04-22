import streamlit as st
import pandas as pd
import numpy as np

#st.cache_data

def convert_df(df):
    return df.to_csv().encode('utf-8')

st.title('EXTRACTION SYNOPTTIQUE')

uploaded_file = st.file_uploader("Choisissez un fichier")

if uploaded_file is not None:
    dict_df = pd.read_excel(uploaded_file,sheet_name=None)
    for index_df in dict_df:
        CHAINE=dict_df[index_df].unstack().dropna().reset_index(drop=True)
        CHAINE_array=CHAINE.values

        #INITIALISATION DES VARIABLES

        ADRESSE_FINAL=[]
        EPISSURE=[]
        LONGUEUR=[]
        CABLE=[]
        MODELE_FINAL=[]
        index_long=[]
        index_cable=[]

        #TRAITEMENT DES REF COMMANDES

        REFCOM=CHAINE[CHAINE.str.contains('F[0-9]{11}',na=False)]
        REFCOM=REFCOM.reset_index(drop=True)

        #TRAITEMENT DES ADRESSES

        ADRESSE=CHAINE[CHAINE.str.contains('[0-9]{5}\s+[^0-9+]',na=False)]
        for adresse in ADRESSE:
            if 'SI' not in adresse:
                ADRESSE_FINAL.append(adresse)

        ADRESSE_FINAL=pd.Series(ADRESSE_FINAL)

        #TRAITEMENT DES EPISSURES

        EPI=CHAINE[CHAINE.str.contains('DROIT|PASSAGE|EPISSURE|RACCORDEMENT',na=False)]

        for index_epi in EPI.index:
            if CHAINE[index_epi+1].startswith('ORF'):
                EPISSURE.append(CHAINE[index_epi])
            elif CHAINE[index_epi+1].startswith('BYT'):
                EPISSURE.append(CHAINE[index_epi])
            elif CHAINE[index_epi+1].startswith('NXL'):
                EPISSURE.append(CHAINE[index_epi])
            elif CHAINE[index_epi+1].startswith('OPE'):
                EPISSURE.append(CHAINE[index_epi])
            elif CHAINE[index_epi+1].startswith('COL'):
                EPISSURE.append(CHAINE[index_epi])
            elif CHAINE[index_epi+1].startswith('BPE'):
                EPISSURE.append(CHAINE[index_epi])
            elif CHAINE[index_epi+1].startswith('BPP'):
                EPISSURE.append(CHAINE[index_epi])
            elif CHAINE[index_epi+1].startswith('BPI'):
                EPISSURE.append(CHAINE[index_epi])

        EPISSURE=pd.Series(EPISSURE)

        #TRAITEMENT DES BPE

        BPEU=CHAINE[CHAINE.str.contains('BPEU[0-9]|BPEA[0-9]|BPP[0-9]|BPI[0-9]|BPEI[0-9]|BPE-V',na=False)]
        BPEU=BPEU.reset_index(drop=True)

        #TRAITEMENT DES MODELES

        MODELE=CHAINE[CHAINE.str.contains('BPEU[0-9]|BPEA[0-9]|BPP[0-9]|BPI[0-9]|BPEI[0-9]|BPE-V',na=False)]

        for index_modele,value_modele in zip(MODELE.index,MODELE.values):
            if CHAINE[index_modele+1].endswith('FR6')|CHAINE[index_modele+1].endswith('FR6 '):
                MODELE_FINAL.append(CHAINE[index_modele+1])
            elif CHAINE[index_modele+1].endswith('HD')|CHAINE[index_modele+1].endswith('HD '):
                MODELE_FINAL.append(CHAINE[index_modele+1])
            elif CHAINE[index_modele+1].endswith('T0')|CHAINE[index_modele+1].endswith('T0 '):
                MODELE_FINAL.append(CHAINE[index_modele+1])
            elif CHAINE[index_modele+1].endswith('T1')|CHAINE[index_modele+1].endswith('T1 '):
                MODELE_FINAL.append(CHAINE[index_modele+1])
            elif CHAINE[index_modele+1].endswith('Taille 0')|CHAINE[index_modele+1].endswith('Taille 0 '):
                MODELE_FINAL.append(CHAINE[index_modele+1])
            elif CHAINE[index_modele+1].endswith('PEO')|CHAINE[index_modele+1].endswith('PEO '):
                MODELE_FINAL.append(CHAINE[index_modele+1])

        MODELE_FINAL=pd.Series(MODELE_FINAL)

        #TRAITEMENT DES SUPPORTS

        CHAMBRE=CHAINE[CHAINE.str.contains('ORF_|BYT_|NXL_|COL_|OPE_|NEX_|POL|ATC_|OPT_',na=False)]
        CHAMBRE=CHAMBRE.reset_index(drop=True)

        #TRAITEMENT DE LA CAPACITE

        CAPACITE=CHAINE[CHAINE.str.contains('288 FO|288 Fo|288 fo|288FO|288Fo|288fo|72 FO|72 Fo|72 fo|72FO|72Fo|72fo|36 FO|36 Fo|36 fo|36FO|36Fo|36fo|24 FO|24 Fo|24 fo|24FO|24Fo|24fo',na=False)]
        CAPACITE=CAPACITE.reset_index(drop=True)

        #TRAITEMENT DES CABLES

        CAB=CHAINE[CHAINE.str.contains('288 FO|288 Fo|288 fo|288FO|288Fo|288fo|72 FO|72 Fo|72 fo|72FO|72Fo|72fo|36 FO|36 Fo|36 fo|36FO|36Fo|36fo|24 FO|24 Fo|24 fo|24FO|24Fo|24fo',na=False)]

        for index_cab in CAB.index:
            if (CHAINE[index_cab+1].startswith('CIU')|CHAINE[index_cab+1].startswith('CDP'))|(CHAINE[index_cab+1].startswith('CIC'))|(CHAINE[index_cab+1].startswith('CSA'))|(CHAINE[index_cab+1].startswith('CAD'))|(CHAINE[index_cab+1].startswith('CDD')):
                index_cable.append(index_cab+1)
            elif (CHAINE[index_cab+1].startswith('CIU')|CHAINE[index_cab+2].startswith('CDP'))|(CHAINE[index_cab+2].startswith('CIC'))|(CHAINE[index_cab+2].startswith('CSA'))|(CHAINE[index_cab+2].startswith('CAD'))|(CHAINE[index_cab+2].startswith('CDD')):
                index_cable.append(index_cab+2)

        for ic in index_cable:
            CABLE.append(CHAINE[ic])

        CABLE=pd.Series(CABLE)

        #TRAITEMENT DES LONGUEURS

        LONG=CHAINE[CHAINE.str.contains('288 FO|288 Fo|288 fo|288FO|288Fo|288fo|72 FO|72 Fo|72 fo|72FO|72Fo|72fo|36 FO|36 Fo|36 fo|36FO|36Fo|36fo|24 FO|24 Fo|24 fo|24FO|24Fo|24fo',na=False)]

        for index_capa in LONG.index:
            index_long.append(index_capa-1)

        for il in index_long:
            LONGUEUR.append(CHAINE[il])

        LONGUEUR=pd.Series(LONGUEUR)

        df_out=pd.concat([CABLE,CAPACITE,LONGUEUR,BPEU,EPISSURE,MODELE_FINAL,CHAMBRE,ADRESSE_FINAL],axis=1)
        df_out=df_out.rename(columns={0:'CABLE',1:'CAPACITE',2:'LONGUEUR',3:'BPEU',4:'EPISSURE',5:'MODELE',6:'CHAMBRE',7:'ADRESSE'})

        st.subheader(index_df)
        st.write(df_out)
        csv=convert_df(df_out)

        st.download_button(
            label='Télécharger',
            data=csv,
            file_name=index_df+'_out.csv',
            mime='text/csv'
        )
