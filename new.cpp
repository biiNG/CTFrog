#include<cstdio>
#include<algorithm>
#define MAXN 110
#define INF 1000000000
using namespace std;
int w1[MAXN],w2[MAXN];
int dp[MAXN][3];
int main(){
	freopen("biconnected.in","r",stdin);
	freopen("biconnected.out","w",stdout);
	int n;
	scanf("%d",&n);
	n+=1;
	int sum=0;
	for(int i=2;i<=n;i++){
		scanf("%d",&w1[i]);
		sum+=w1[i];
	}
	for(int i=3;i<=n;i++){
		scanf("%d",&w2[i]);
		sum+=w2[i];
	}
	if(n==3){
		printf("%d\n",sum);
		return 0;
	}
	dp[3][0]=0;
	dp[3][1]=w1[1];
	dp[3][2]=-INF;
	for(int i=4;i<n;i++){
		dp[i][0]=max(dp[i-1][0],max(dp[i-1][1],dp[i-1][2]));
		dp[i][1]=max(dp[i-1][0],dp[i-1][2])+w1[i];
		dp[i][2]=max(dp[i-1][0],dp[i-1][1])+w2[i];
	}
	printf("%d\n",sum-max(dp[n-1][0],max(dp[n-1][1],dp[n-1][2])));
}