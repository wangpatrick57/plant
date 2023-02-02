#!/bin/sh
G1=$1; G2=$2; CCG=$3
TAB='	'
cat "$3" | sed "s/ /$TAB/" -e 's/[()]//g' -e 's/,/ /g' |
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
	    for(u1 in E[3])for(v1 in E[3][u1]) {
		ASSERT(u1>v1,"u1>v1");
		ASSERT(E[1][u1][v1],"E[1][u1][v1] "u1" "v1" "1*E[1][u1][v1]);
		u2=A[u1];v2=A[v1]; U2=MAX(u2,v2); V2=MIN(u2,v2);
		ASSERT(E[2][U2][V2], "E[2][U2][V2] "U2" "V2" "1*E[2][U2][V2]);
		ASSERT(DEG[1][u1]>=DEG[3][u1]); ASSERT(DEG[2][u2]>=DEG[4][u2]);
		ASSERT(DEG[1][v1]>=DEG[3][v1]); ASSERT(DEG[2][v2]>=DEG[4][v2]);
		printf "u1 u2\tv1 v2 = %s %s\t%s %s; degrees %d(%d) %d(%d)\t%d(%d) %d(%d)\n",
		                       u1,u2, v1,v2, DEG[1][u1],DEG[3][u1],DEG[2][u2],DEG[4][u2],
				                     DEG[1][v1],DEG[3][v1],DEG[2][v2],DEG[4][v2]
	    }
	}' "$1" "$2" -
