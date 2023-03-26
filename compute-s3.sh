#/bin/sh -x
################## SKELETON: DO NOT TOUCH THESE 2 LINES
BASENAME=`basename "$0" .sh`; TAB='	'; NL='
'
#################### ADD YOUR USAGE MESSAGE HERE, and the rest of your code after END OF SKELETON ##################
USAGE="USAGE: $BASENAME net1.el net2.el alignment-file
PURPOSE: given two networks and a 1-to-1 alignment, compute the S3 (Symmetric Substructure) Score."

################## SKELETON: DO NOT TOUCH CODE HERE
# check that you really did add a usage message above
USAGE=${USAGE:?"$0 should have a USAGE message before sourcing skel.sh"}
die(){ echo "$USAGE${NL}FATAL ERROR in $BASENAME:" "$@" >&2; exit 1; }
[ "$BASENAME" == skel ] && die "$0 is a skeleton Bourne Shell script; your scripts should source it, not run it"
echo "$BASENAME" | grep "[ $TAB]" && die "Shell script names really REALLY shouldn't contain spaces or tabs"
[ $BASENAME == "$BASENAME" ] || die "something weird with filename in '$BASENAME'"
warn(){ (echo "WARNING: $@")>&2; }
not(){ if eval "$@"; then return 1; else return 0; fi; }
newlines(){ awk '{for(i=1; i<=NF;i++)print $i}' "$@"; }
parse(){ awk "BEGIN{print $*}" </dev/null; }

# Temporary Filename + Directory (both, you can use either, note they'll have different random stuff in the XXXXXX part)
TMPDIR=`mktemp -d /tmp/$BASENAME.XXXXXX`
#trap "/bin/rm -rf $TMPDIR; exit" 0 1 2 3 15 # call trap "" N to remove the trap for signal N

#################### END OF SKELETON, ADD YOUR CODE BELOW THIS LINE
net1="$1"
net2="$2"
align="$3"

$SANA/sana -fg1 "$net1" -fg2 "$net2" -s3 1 -mode analysis -alignFile "$align" -alignFormat 3 -o $TMPDIR/s3 >$TMPDIR/s3.stdout 2>$TMPDIR/s3.stderr
grep "^s3:" $TMPDIR/s3.out
exit

hawk 'ARGIND<=2{edge[ARGIND][$1][$2]=edge[ARGIND][$2][$1]=1}
    ARGIND==3{A1[FNR]=$1; A2[FNR]=$2}
    END{
	ASSERT(length(edge[1]) <= length(edge[2]), "net1 must have <= nodes of net2");
	n=length(A1);
	ASSERT(n==FNR, "length mismatch");
	for(i=1;i<n;i++) {
	    u1=A1[i]; u2=A2[i];
	    for(j=2;j<=n;j++) {
		v1=A1[j]; v2=A2[j];
		if(edge[1][u1][v1] && edge[2][u2][v2]) {++numer; ++denom;}
		else if(edge[1][u1][v1]) ++denom;
		else if(edge[2][u2][v2]) ++denom;
	    }
	}
	printf "%g = %d / %d\n", numer/denom, numer, denom
    }' "$@"
