#!/bin/bash 

cat imputetemp/${1}-2_impute_filtered | awk '{split($2,a,":"); $2="2:"a[2]"_"a[3]"_"a[4]; print $1,$2,$3,$4,$5}' > imputetemp/${1}-2_awk.gen
cat imputetemp/${1}-3_impute_filtered | awk '{split($2,a,":"); $2="3:"a[2]"_"a[3]"_"a[4]; print $1,$2,$3,$4,$5}' > imputetemp/${1}-3_awk.gen
cat imputetemp/${1}-6_impute_filtered | awk '{split($2,a,":"); $2="6:"a[2]"_"a[3]"_"a[4]; print $1,$2,$3,$4,$5}' > imputetemp/${1}-6_awk.gen
cat imputetemp/${1}-7_impute_filtered | awk '{split($2,a,":"); $2="7:"a[2]"_"a[3]"_"a[4]; print $1,$2,$3,$4,$5}' > imputetemp/${1}-7_awk.gen
cat imputetemp/${1}-8_impute_filtered | awk '{split($2,a,":"); $2="8:"a[2]"_"a[3]"_"a[4]; print $1,$2,$3,$4,$5}' > imputetemp/${1}-8_awk.gen
cat imputetemp/${1}-12_impute_filtered | awk '{split($2,a,":"); $2="12:"a[2]"_"a[3]"_"a[4]; print $1,$2,$3,$4,$5}' > imputetemp/${1}-12_awk.gen
cat imputetemp/${1}-17_impute_filtered | awk '{split($2,a,":"); $2="17:"a[2]"_"a[3]"_"a[4]; print $1,$2,$3,$4,$5}' > imputetemp/${1}-17_awk.gen
cat imputetemp/${1}-19_impute_filtered | awk '{split($2,a,":"); $2="19:"a[2]"_"a[3]"_"a[4]; print $1,$2,$3,$4,$5}' > imputetemp/${1}-19_awk.gen


for file in imputetemp/*impute_filtered*;
do
useridchr=${file##*/}
useridchr=${useridchr%%_*}
chr=${useridchr##*-}
userid=${useridchr%%-*}

gzip imputetemp/${useridchr}_awk.gen 


bcftools convert --gensample2vcf imputetemp/${useridchr}_awk > imputetemp/${useridchr}_imputed.vcf

sed "/#/d" imputetemp/${useridchr}_imputed.vcf > imputetemp/${useridchr}_nohash.vcf

grep "#" imputetemp/${useridchr}_imputed.vcf > imputetemp/${useridchr}_header.vcf

paste imputetemp/${useridchr}_nohash.vcf imputetemp/rsidfile${chr} | awk '{print $1"\t"$2"\t"$9"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8}' > imputetemp/${useridchr}_rsid.vcf

done

cat imputetemp/${userid}-2_header.vcf imputetemp/${userid}-2_rsid.vcf imputetemp/${userid}-3_rsid.vcf imputetemp/${userid}-6_rsid.vcf imputetemp/${userid}-7_rsid.vcf imputetemp/${userid}-8_rsid.vcf imputetemp/${userid}-12_rsid.vcf imputetemp/${userid}-17_rsid.vcf imputetemp/${userid}-19_rsid.vcf > ${userid}_final.vcf

cp ${userid}_final.vcf ..
