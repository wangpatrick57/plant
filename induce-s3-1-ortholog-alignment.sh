#!/bin/bash
USAGE="$0 IID-species1.el IID-species2.el sana.ccs-el
PURPOSE: given two IID species, we assume you've created the 'perfect' alignment file using the \$Max table;
and then you've run sana -mode analysis on said file to produce a sana.ccs-el output file (you may need to
remove duplicate nodes in the alignment file to make SANA happy--pick the higher degree nodes when there's amgituity),
then this script finds the subset of nodes in the CCS file where the s3 score is exactly 1."

# Functions
die(){ (echo "USAGE: $USAGE"; echo "${NL}FATAL ERROR in `basename $0`: $@")>&2; exit 1; }
warn(){ (echo "WARNING: $@")>&2; }
newlines(){ awk '{for(i=1; i<=NF;i++)print $i}' "$@"; }

# generally useful Variables
NL='
'
TAB='	'

G1=$1; G2=$2; CCS="$3"
[ $# -eq 3 ] || die "expecting 3 arguments"
[ -f "$G1" ] || die "no file $G1"
[ -f "$G2" ] || die "no file $G2"
[ -f "$CCS" ] || die "no file $CCS"

# Temporary Filename + Directory (both, you can use either, note they'll have different random stuff in the XXXXXX part)
TMPDIR=`mktemp -d /tmp/$BASENAME.XXXXXX`
trap "/bin/rm -rf $TMPDIR; exit" 0 1 2 3 15 # call trap "" N to remove the trap for signal N

cat "$CCS" | sed "s/ /$TAB/" | sed 's/[()]//g' | sed 's/,/ /g' | awk '{V[$1]=V[$3]=1}END{for(u in V)print u}' > $TMPDIR/G1.nodes
cat "$CCS" | sed "s/ /$TAB/" | sed 's/[()]//g' | sed 's/,/ /g' | awk '{V[$2]=V[$4]=1}END{for(u in V)print u}' > $TMPDIR/G2.nodes

induce $TMPDIR/G1.nodes "$G1" > $TMPDIR/G1-induced.el
induce $TMPDIR/G2.nodes "$G2" > $TMPDIR/G2-induced.el


cat "$CCS" | sed "s/ /$TAB/" | sed 's/[()]//g' | sed 's/,/ /g' |
    hawk 'ARGIND<3{u=MAX($1,$2);v=MIN($1,$2);
	    ++DEG[ARGIND][u]; ++DEG[ARGIND][v]; E[ARGIND][u][v]=1
	}
	ARGIND==3{
	    A[$1]=$2;A[$3]=$4;
	    for(i=1;i<=2;i++) {
		++DEG[2+i][$i]; ++DEG[2+i][$(i+2)];
		u=MAX($i,$(i+2)); v=MIN($i,$(i+2));
		E[2+i][u][v]=1;
	    }
	}
	END{
	    for(u1 in E[3]){
            for(v1 in E[3][u1]) {
                ASSERT(u1>v1,"u1>v1");
                ASSERT(E[1][u1][v1],"E[1][u1][v1] "u1" "v1" "1*E[1][u1][v1]);
                u2=A[u1];v2=A[v1]; U2=MAX(u2,v2); V2=MIN(u2,v2);
                #printf "u1 v1 u2 v2 %s %s %s %s\n", u1,v1,u2,v2
                ASSERT(E[2][U2][V2], "E[2][U2][V2] "U2" "V2" "1*E[2][U2][V2]);
                ASSERT(DEG[1][u1]>=DEG[3][u1]); ASSERT(DEG[2][u2]>=DEG[4][u2]);
                ASSERT(DEG[1][v1]>=DEG[3][v1]); ASSERT(DEG[2][v2]>=DEG[4][v2]);
                if(DEG[1][u1]==DEG[3][u1] && DEG[2][u2]==DEG[4][u2] &&
                   DEG[1][v1]==DEG[3][v1] && DEG[2][v2]==DEG[4][v2])
                   printf "%s %s\t%s %s\n", u1,u2,v1,v2
            }
        }
	}' $TMPDIR/G1-induced.el $TMPDIR/G2-induced.el -
