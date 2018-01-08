#!/bin/bash

##########################################################################################
#																						 #
#						toxsign_enrich													 #
#			Launch go and disease enrichment for toxsign signatures      				 #
#			DO NOT edit this file														 #
#			edit config.ini instead														 #
##########################################################################################


#Source config file
#source: WORK_DIR variable
#		 SCRIPT_DIR variable
#		 SIGNATURE_PATH variable
source config.ini

#variables
#
# -q genome query Q_GENOME (bam file genome)
# -n name STUDY_NAME
# -t genome target T_GENOME
# -i bam input BAM_INPUT

# config variables
#WORK_DIR="/home/genouest/irset/tdarde/workDir/"
#SCRIPT_DIR="/home/genouest/irset/tdarde/workDir/sys/script/"
#SIGNATURE_PATH="/home/genouest/irset/tdarde/workDir/signature_data/"
#ANNOTATION_PATH="/home/genouest/irset/tdarde/workDir/sys/annotation/"
#LOG_PATH="/home/genouest/irset/tdarde/workDir/sys/log/"




function annotation {
#Create homologene2go file
logout=$LOG_PATH"TXS_homologene2Go_.out"
qsub -N "TXS_homologene2Go" -j y -o $logout $SCRIPT_DIR"qsub_wish.sh" $SCRIPT_DIR"homologene2go.tcl" $ANNOTATION_PATH"homologene.data" $ANNOTATION_PATH"gene2go" $ANNOTATION_PATH"gene_ontology.obo" $ANNOTATION_PATH
qsub -N "TXS_homologene2hpo" -j y -o $logout $SCRIPT_DIR"qsub_h2hpo.sh" $SCRIPT_DIR $ANNOTATION_PATH"homologene.data" $ANNOTATION_PATH"ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt" $ANNOTATION_PATH"hp.obo" $ANNOTATION_PATH
qsub -N "TXS_homologene2MPO" -j y -o $logout $SCRIPT_DIR"qsub_h2mpo.sh" $SCRIPT_DIR $ANNOTATION_PATH"homologene.data" $ANNOTATION_PATH"MGI_Gene_Model_Coord.rpt" $ANNOTATION_PATH"MGI_PhenoGenoMP.rpt" $ANNOTATION_PATH"MPheno_OBO.ontology"  $ANNOTATION_PATH

#Waiting for the end of homologene2go file creation
while [ $(qstat | grep "TXS_ho" | wc -l) -ne 0 ]
	do
		echo "Running TXS_homologene2Go"
		sleep 7
done

#Create one annotation file
rm $ANNOTATION_PATH"annotation"
cat $ANNOTATION_PATH"homologene2go" >> $ANNOTATION_PATH"annotation"
cat $ANNOTATION_PATH"homologene2mpo" >> $ANNOTATION_PATH"annotation"
cat $ANNOTATION_PATH"homologene2hpo" >> $ANNOTATION_PATH"annotation"
}

function Enrich {
x=1
# Find all new signatures
for i in $(find $SIGNATURE_PATH -name "[^.]*.txt"  -newer $SCRIPT_DIR"dateref")
	do
	echo $i
	OUTPUT_FILE=$i".enr"
	FINAL_FILE=$i".enr"
	logout=$LOG_PATH"TXS_prepEnrich_"$x".out"
	qsub -N "TXS_prepEnrich_$x" -j y -o $logout $SCRIPT_DIR"qsub_prepEnrich.sh" $ANNOTATION_PATH"annotation" $i $OUTPUT_FILE $SCRIPT_DIR $FINAL_FILE
	let "x = $x + 1"
done

#Waiting for the end of homologene2go file creation
while [ $(qstat | grep "TXS_prep" | wc -l) -ne 0 ]
	do
		echo "Running TXS_prepEnrich"
		sleep 7
done


touch -a $SCRIPT_DIR"dateref"
echo "TXS_prepEnrich done"
}

################################################################################
#Main
if [ $# != 0 ] && [ $1 = "--annot" ]
then 
	echo "ANNOT"
	annotation
	Enrich
else
	echo "NO ANNOT"
	Enrich
fi
