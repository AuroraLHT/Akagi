%background data import

fixeddata;
importCPI;
importGDP;
importLPR;
importMG_SH;
importMS;
importPPI;
importRRR;
importSHIBOR;
importSH_Index;

GDP={GDP_Q,gdp_yoy,pi_yoy,si_yoy,ti_yoy};
CPI={CPI_M,cpi};
SHIBOR={SHIBOR_D,ON,OW,TW,OM,TRM,SIM,NM,OY};
LPR={LPR_D,LPR_OY};
PPI={PPI_M,ppiip,ppi,qm,rmi,pi1,cg,food,clothing,roeu,dcg};
MS={MS_M,m2_yoy,m1_yoy,m0_yoy,cd1,qm1,ftd,sd,rests};
rrr={RRR,now1};
SHMargin={SHMargin_D,rzye,rzmre,rqyl,rqylje,rqmcl,rzrqjyzl};
SH_Index={SH_date,SH_open,SH_close,SH_volume};

clearvars -except GDP CPI SHIBOR LPR PPI MS rrr SHMargin SH_Index sheetname figsavepath stockpath