#!/usr/bin/wish
package require Tcl 8.6
# Please donwload the mammalian phenotype ontology and the association file at:
#http://www.informatics.jax.org/downloads/reports/MGI_Gene_Model_Coord.rpt
#http://www.informatics.jax.org/downloads/reports/MPheno_OBO.ontology
#http://www.informatics.jax.org/downloads/reports/MGI_PhenoGenoMP.rpt
##############################################################################
# OBO.tcl - procedures used by AMEN to parse and to query ontology databases
# using the OBO v1.2 file format.
#
# OBO library package for Tcl 8.5+. Written by Frédéric Chalmel
#
# Copyright (c) 2009, Frédéric Chalmel
# All Rights Reservered
#
# Author contact information:
#   frederic.chalmel@inserm.fr
#   http://www.nantes.inserm.fr/membres/unite625/m_pages.asp?page=1053&menu=395
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU
# Library General Public License for more details.
# 
# core OBO support:
#    ::OBO::Example
#    ::OBO::Load <file>
#    ::OBO::Delete <?file>
#    ::OBO::Unset  <file> <arg1> <arg2> ...
#    ::OBO::Query  <file> <arg1> <arg2> ...
#    ::OBO::Exists <file> <arg1> <arg2> ...	
#    ::OBO::Parents       <file> <ListOfTerms> <?WithChildren>
#    ::OBO::Children      <file> <ListOfTerms> <?WithParents>
#    ::OBO::UpperChildren <file> <ListOfTerms>
#
# Internal procedures
#    OBO::Parents_Recursif  <file> <Term> <?ListOfParentTerms>
#    OBO::Children_Recursif <file> <Term> <?ListOfChildrenTerms>
#
# Revision history:
#    FC 2009/03/23 - version 1.0 is out!
#
# TODO:
#               
#
##############################################################################

package provide OBO 1.0

namespace eval ::OBO {
    variable TabOBOPanel
    proc Example {} {
	variable TabOBOPanel
	set OBOFile "/sfs1/home/frt/fchalmel/data/Ontologies/gene_ontology.obo"
	::OBO::Load   $OBOFile
	foreach OBOID [::OBO::Parents $OBOFile "GO:0022408"] {
	    puts "$OBOID -> [::OBO::Query $OBOFile Term $OBOID name] -> [::OBO::Query $OBOFile Term $OBOID namespace]"
	    puts "$OBOID -> [::OBO::Query $OBOFile Term $OBOID Synonym]"
	}
	::OBO::Delete $OBOFile

	return
    }
    proc Load {OBOFile} {
	variable TabOBOPanel
	if {![file exists $OBOFile]} {
	    puts stderr "$OBOFile does not exist!"
	    return 0
	}
	puts stdout "$OBOFile is loading..."
	
	set TabOBOPanel($OBOFile,LOADED) 1

	set InATermDefinition 0
	set InATypeDefinition 0
	set CurrentID         ""
	
	if {![info exists TabOBOPanel($OBOFile,Term)   ]} {set TabOBOPanel($OBOFile,Term)    {}}
	if {![info exists TabOBOPanel($OBOFile,Typedef)]} {set TabOBOPanel($OBOFile,Typedef) {}}
	
	set F [open $OBOFile]
	while {[gets $F Line]>=0} {
	    set Line   [string trim $Line]
	    set lLine  [split $Line ":"]
	    set HEADER    [lindex $lLine 0]
	    if {$HEADER == ""} {continue}
	    set REMAINDER [string trim [join [lrange $lLine 1 end] ":"]]
	    if {$HEADER == "\[Term\]"} {
		set InATermDefinition 1
		set InATypeDefinition 0
		set CurrentID         ""
		continue
	    }
	    if {$HEADER == "\[Typedef\]"} {
		set InATermDefinition 0
		set InATypeDefinition 1
		set CurrentID         ""
		continue
	    }
	    if {$InATermDefinition} {
		set TYPE "Term"
	    } elseif {$InATypeDefinition} {
		set TYPE "Typedef"
	    } else {
		if {![info exists TabOBOPanel($OBOFile,$HEADER)]} {set TabOBOPanel($OBOFile,$HEADER) {}}
		lappend TabOBOPanel($OBOFile,$HEADER) $REMAINDER
		continue
	    }
	    
	    if {$HEADER == "id"} {
		set     CurrentID                              [lindex [split $REMAINDER " "] 0]
		lappend TabOBOPanel($OBOFile,$TYPE)            $CurrentID
		set     TabOBOPanel($OBOFile,$TYPE,$CurrentID) $CurrentID
		continue
	    }
	    if {$CurrentID == ""} {continue}
	    
	    if {      $HEADER == "alt_id"      } {
		set ALTID [string trim [lindex [split $REMAINDER " "] 0]]
		set       TabOBOPanel($OBOFile,$TYPE,$ALTID) $CurrentID
		continue
	    } 
	    if {$HEADER == "is_a" || $HEADER == "relationship"} {
		set lREMAINDER [split $REMAINDER " "]
		if {$HEADER == "is_a"} {
		    set Relation  "is_a"
		    set RelatedID [string trim [lindex $lREMAINDER 0]]
		} else {
		    set Relation  [string trim [lindex $lREMAINDER 0]]
		    set RelatedID [string trim [lindex $lREMAINDER 1]]
		}
		if {$Relation == "is_a" || $Relation == "part_of"} {
		    if {![info exists TabOBOPanel($OBOFile,$TYPE,$CurrentID,Parents) ]} {set TabOBOPanel($OBOFile,$TYPE,$CurrentID,Parents)  {}}
		    if {![info exists TabOBOPanel($OBOFile,$TYPE,$RelatedID,Children)]} {set TabOBOPanel($OBOFile,$TYPE,$RelatedID,Children) {}}
		    lappend TabOBOPanel($OBOFile,$TYPE,$CurrentID,Parents)  $RelatedID
		    lappend TabOBOPanel($OBOFile,$TYPE,$RelatedID,Children) $CurrentID
		}
		if {![info exists TabOBOPanel($OBOFile,$TYPE,$CurrentID,Relationship)]} {set TabOBOPanel($OBOFile,$TYPE,$CurrentID,Relationship) {}}
		lappend TabOBOPanel($OBOFile,$TYPE,$CurrentID,Relationship) [list $RelatedID $Relation]
		continue
	    }

	    if {![info exists TabOBOPanel($OBOFile,$TYPE,$CurrentID,$HEADER)]} {set TabOBOPanel($OBOFile,$TYPE,$CurrentID,$HEADER) {}}
	    lappend TabOBOPanel($OBOFile,$TYPE,$CurrentID,$HEADER) $REMAINDER

	    if {[regexp {synonym} $HEADER]} {
		set HEADER "Synonym"
		if {![info exists TabOBOPanel($OBOFile,$TYPE,$CurrentID,$HEADER)]} {set TabOBOPanel($OBOFile,$TYPE,$CurrentID,$HEADER) {}}
		lappend TabOBOPanel($OBOFile,$TYPE,$CurrentID,$HEADER) $REMAINDER
	    }
	}
	close $F

	puts stdout "$OBOFile is loaded."
	return 1
    }
    proc Delete {{OBOFile ""}} {
	variable TabOBOPanel
	if {![info exists TabOBOPanel]} {return 0}

	if {$OBOFile != ""} {
	    foreach index [array names TabOBOPanel "$OBOFile,*"] {unset TabOBOPanel($index)}
	} else {
	    unset TabOBOPanel
	}
	return 1
    }
    proc Unset args {
	variable TabOBOPanel
	set ARG [join [lrange $args 0 end] ","]
	if {![info exists TabOBOPanel($ARG)]} {return 0}
	unset TabOBOPanel($ARG) 
	return 1
    }
    proc Query args {
	variable TabOBOPanel
	set ARG [join [lrange $args 0 end] ","]
	if {![info exists TabOBOPanel($ARG)]} {return}
	return [ListOfNonRedundantElement $TabOBOPanel($ARG)]
    }
    proc Exists args {
	variable TabOBOPanel
	set ARG [join [lrange $args 0 end] ","]
	if {![info exists TabOBOPanel($ARG)]} {return 0}
	return 1
    }
    proc Parents {OBOFile ListOfOBOIDs {WithChildren 1}} {
	set ListOfParentOBOIDs {}
	foreach OBOID [ListOfNonRedundantElement $ListOfOBOIDs] {
	    set OBOID [::OBO::Query $OBOFile Term $OBOID]
	    foreach ParentOBOID [::OBO::Parents_Recursif $OBOFile $OBOID] {
		if {[info exists TabDejaVu($ParentOBOID)]} {continue}
		set TabDejaVu($ParentOBOID) 1
		lappend ListOfParentOBOIDs $ParentOBOID
	    }
	}
	if {$WithChildren} {
	    return [ListOfNonRedundantElement [concat $ListOfOBOIDs $ListOfParentOBOIDs]]
	} else {
	    return [ListOfNonRedundantElement $ListOfParentOBOIDs]
	}
    }
    proc Children {OBOFile ListOfOBOIDs {WithParents 1}} {
	set ListOfChildOBOIDs {}
	foreach OBOID [ListOfNonRedundantElement $ListOfOBOIDs] {
	    set OBOID [::OBO::Query $OBOFile Term $OBOID]
	    foreach ChildOBOID [::OBO::Children_Recursif $OBOFile $OBOID] {
		if {[info exists TabDejaVu($ChildOBOID)]} {continue}
		set TabDejaVu($ChildOBOID) 1
		lappend ListOfChildOBOIDs $ChildOBOID
	    }
	}
	if {$WithParents} {
	    return [ListOfNonRedundantElement [concat $ListOfOBOIDs $ListOfChildOBOIDs]]
	} else {
	    return [ListOfNonRedundantElement $ListOfChildOBOIDs]
	}
    }
    proc UpperChildren {OBOFile ListOfOBOIDs} {
	foreach OBOID [::OBO::Parents $OBOFile $ListOfOBOIDs 0] {set TabDejaVu($OBOID) 1}
	
	set ListOfTermWithoutParent {}
	foreach OBOID $ListOfOBOIDs {
	    if {[info exists TabDejaVu($OBOID)]} {continue}
	    lappend ListOfTermWithoutParent $OBOID
	}
	return $ListOfTermWithoutParent
    }
    proc Parents_Recursif {OBOFile ParentOBOID {ListOfParentOBOIDs {}}} {
	foreach OBOID $ListOfParentOBOIDs {set TabDejaVu($OBOID) 1}
	foreach OBOID [::OBO::Query $OBOFile Term $ParentOBOID Parents] {
	    set OBOID [::OBO::Query $OBOFile Term $OBOID]
	    if {[info exists TabDejaVu($OBOID)]} {continue}
	    lappend ListOfParentOBOIDs $OBOID
	    set ListOfParentOBOIDs [::OBO::Parents_Recursif $OBOFile $OBOID $ListOfParentOBOIDs]
	}
	return $ListOfParentOBOIDs
    }
    proc Children_Recursif {OBOFile ParentOBOID {ListOfChildOBOIDs {}}} {
	foreach OBOID $ListOfChildOBOIDs {set TabDejaVu($OBOID) 1}
	foreach OBOID [::OBO::Query $OBOFile Term $ParentOBOID Children] {
	    set OBOID [::OBO::Query $OBOFile Term $OBOID]
	    if {[info exists TabDejaVu($OBOID)]} {continue}
	    lappend ListOfChildOBOIDs $OBOID
	    set ListOfChildOBOIDs [::OBO::Children_Recursif $OBOFile $OBOID $ListOfChildOBOIDs]
	}
	return $ListOfChildOBOIDs
    }
}
##############################################################################

##############################################################################
namespace eval ::File {
    proc Open {File {N 100} {Complete "no"}} {
	variable Tab
	### if 'Complete' = yes, the information are added at the end of the file ###
	if {[string compare -nocase $Complete "yes"]} {set option "w"} else {set option "a"}
	set Channel          [open $File $option]
	set Tab($File)       $Channel
	set Tab($File,Lines) {}
	set Tab($File,N)     $N	
	return 1
    }
    proc Save {File Text {Complete "no"}} {
	### if 'Complete' = yes, the information are added at the end of the file ###
	variable Tab
	if {![info exists Tab($File)]} {
	    ::File::Open  $File 0     $Complete
	    ::File::Save  $File $Text $Complete
	    ::File::Close $File
	} else {
	    lappend Tab($File,Lines) $Text
	    if {$Tab($File,N) <= [llength $Tab($File,Lines)]} {
		puts $Tab($File)      [join $Tab($File,Lines) "\n"]
		set  Tab($File,Lines) {}
	    }
	}
	return $File
    }
    proc Close {File} {
	variable Tab
	if {[info exists Tab($File)] && [info exists Tab($File,Lines)]} {
	    if {0 < [llength $Tab($File,Lines)]} {
		puts $Tab($File) [join $Tab($File,Lines) "\n"]
	    }
	    close $Tab($File)

	    catch {unset Tab($File) Tab($File,Lines) Tab($File,N)}
	    return 1
	} else {
	    return 0
	}
    }
}
##############################################################################

##############################################################################
proc ListOfNonRedundantElement {Liste} {
    set ListOfNonRedundant {}
    foreach Elt $Liste {
	if {[info exists TabDejaVu($Elt)]} {continue}
	set     TabDejaVu($Elt)     1
	lappend ListOfNonRedundant $Elt
    }
    return $ListOfNonRedundant
}
##############################################################################

set HomoloGeneFile ""
set Gene2MGIFile   ""
set MGI2MPOFile    ""
set MPOOBOFile     ""
set OutDir         ""

for {set i 0} {$i < [llength $argv]} {incr i} {
    set What [lindex $argv $i]
    if {$What == "-h"} {
	puts "homologene2mpo.tcl, v. 1.0"
        puts "Command line:\nwish homologene2mpo.tcl -hg \[homologene.data file\] -gene2mgi \[gene2mgi file\] -mgi2mpo \[mgi2mpo file\] -mpoobo \[mp.obo file\] -o \[output directory\]"
        exit
    }
    if {$What == "-hg"} {
	incr i
	set HomoloGeneFile [lindex $argv $i]
    }
    if {$What == "-mgi2mpo"} {
	incr i
	set MGI2MPOFile [lindex $argv $i]
    } 
    if {$What == "-gene2mgi"} {
	incr i
	set Gene2MGIFile [lindex $argv $i]
    } 
    if {$What == "-mpoobo"} {
	incr i
	set MPOOBOFile [lindex $argv $i]
    } 
     if {$What == "-o"} {
	incr i
	set OutDir [lindex $argv $i]
    }
}
if {$HomoloGeneFile == "" || ![file exists $HomoloGeneFile]} {
    puts stderr "The homologene.data file does not exist: $HomoloGeneFile"
    exit
}
if {$Gene2MGIFile == "" || ![file exists $Gene2MGIFile]} {
    puts stderr "The gene2mgi file does not exist: $Gene2MGIFile"
    exit
}
if {$MGI2MPOFile == "" || ![file exists $MGI2MPOFile]} {
    puts stderr "The mgi2mpo file does not exist: $MGI2MPOFile"
    exit
}
if {$MPOOBOFile == "" || ![file exists $MPOOBOFile]} {
    puts stderr "The hp.obo file does not exist: $MPOOBOFile"
    exit
}
if {$OutDir == "" || ![file exists $OutDir]} {
    puts stderr "The output directory does not exist: $OutDir"
    exit
}

#----------------------------------#
set ListOfMPOTypes [list Phenotype]
set ListOfHGIDs   {}
puts "$HomoloGeneFile is loading..."
set F [open $HomoloGeneFile]
while {[gets $F Line]>=0} {
    set HGID ""
    foreach {HGID TAXID GENEID GENESYMB} [lrange [split $Line "\t"] 0 3] {}
    if {$HGID == ""} {continue}
    set TabGeneID2HGID($GENEID) $HGID
    foreach MPOType $ListOfMPOTypes {
	set TabHGID2MPOID($HGID,$MPOType)     {}
    }
    lappend ListOfHGIDs $HGID
}
close $F
puts "$HomoloGeneFile loaded!"
#----------------------------------#

#----------------------------------#
puts "$Gene2MGIFile is loading..."
set i 0
set F [open $Gene2MGIFile]
while {[gets $F Line]>=0} {
    incr i
    if {$i == 1} {continue}
    set GENEID ""
    foreach {MGIID TYPE GENESYMB GENENAME BUILD GENEID} [lrange [split $Line "\t"] 0 5] {}
    if {$GENEID == "" || $GENEID == "null"} {continue}
    if {![info exists TabGeneID2HGID($GENEID)]} {continue}
    set TabMGIID2HGID($MGIID) $TabGeneID2HGID($GENEID)
}
close $F
puts "$Gene2MGIFile loaded!"
#----------------------------------#


#----------------------------------#
puts "$MGI2MPOFile is loading..."
set F [open $MGI2MPOFile]
while {[gets $F Line]>=0} {
    set MGIID ""
    foreach {MPOID PMID MGIID} [lrange [split $Line "\t"] 3 5] {}
    if {$MGIID == ""} {continue}
    if {![info exists TabMGIID2HGID($MGIID)]} {continue}
    set HGID $TabMGIID2HGID($MGIID)
    lappend TabHGID2MPOID($HGID,Phenotype) $MPOID
}
close $F
puts "$MGI2MPOFile loaded!"
#----------------------------------#

#----------------------------------#
set OutFile "$OutDir/homologene2mpo"
::OBO::Load   $MPOOBOFile
puts "$OutFile is saving..."
::File::Open  $OutFile 1000 "no"
foreach MPOType $ListOfMPOTypes {
    foreach HGID [ListOfNonRedundantElement $ListOfHGIDs] {
	set MPOIDs [ListOfNonRedundantElement $TabHGID2MPOID($HGID,$MPOType)]
	foreach MPOID [::OBO::Parents $MPOOBOFile $MPOIDs] {
	    set MPOTerm [lindex [::OBO::Query $MPOOBOFile Term $MPOID name] 0]
	    if {$MPOTerm == ""} {continue}
	    ::File::Save $OutFile "$HGID\t$MPOType\t$MPOTerm ($MPOID)"
	}
    }
}
::File::Close $OutFile
puts "$OutFile saved!"
::OBO::Delete $MPOOBOFile
#----------------------------------#


exit
