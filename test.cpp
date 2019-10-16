#include<cstdio>
#include<cstring>
#include<algorithm>
using namespace std;
template<class T>
void read(T &x)
{
	char c;
	while(c=getchar(),c!=EOF)
		if(c>='0'&&c<='9')
		{
			x=c-'0';
			while(c=getchar(),c>='0'&&c<='9')x=x*10+c-'0';
			ungetc(c,stdin);
			return ;
		}
}
#define MAXN 500010
typedef long long ll;
int n,a[MAXN],b[MAXN],que[MAXN];
ll sum[MAXN],dp[2][MAXN];
pair<ll,ll>q[MAXN];
bool cmp(int x,int y){return b[x+1]<b[y+1];}
void init()
{
	read(n);
	for(int i=1;i<=n;i++)
	{
		read(a[i]);
		sum[i]=sum[i-1]+a[i];
	}
	for(int i=1;i<=n;i++)
		read(b[i]);
}
void reverse()
{
	for(int i=1,j=n;i<=n/2;i++,j--)
		swap(a[i],a[j]),swap(b[i],b[j]);
	for(int i=1;i<=n;i++)
		sum[i]=sum[i-1]+a[i];
}
int query(int l,int r,int B)
{
	if(l==r)return l;
	l++;
	int mid;
	while(l<r)
	{
		mid=(l+r)>>1;
		if(sum[que[mid-1]]-sum[que[mid]]<=1ll*(que[mid-1]-que[mid])*B)l=mid+1;
		else r=mid;
	}
	if(sum[que[r-1]]-sum[que[r]]>1ll*(que[r-1]-que[r])*B)return r-1;
	else return r;
}
void CDQ(int l,int r,int f)
{
	if(l==r)return ;
	int mid=(l+r)>>1;
	CDQ(l,mid,f);
	CDQ(mid+1,r,f);
	for(int i=l;i<=mid;i++)que[i]=i;
	sort(que+l,que+mid+1,cmp);
	int front=1,rear=1;
	q[front].first=1ll*b[que[l]+1];
	q[front].second=sum[que[l]]-1ll*que[l]*b[que[l]+1];
	for(int i=l+1;i<=mid;i++)
	{
		ll x=1ll*b[que[i]+1],y=sum[que[i]]-1ll*que[i]*b[que[i]+1];
		while(front<rear&&(double)(q[rear].second-q[rear-1].second)/(double)(q[rear].first-q[rear-1].first)<=(double)(1ll*y-q[rear].second)/(double(1ll*x-q[rear].first)))rear--;
		//while(front<rear&&(q[rear].second-q[rear-1].second)*(1ll*x-q[rear].first)<=(q[rear].first-q[rear-1].first)*(1ll*y-q[rear].second))rear--;
		rear++;
		q[rear].first=x,q[rear].second=y;
	}
	for(int i=mid+1;i<=r;i++)
	{
		while(front<rear&&q[front+1].second-q[front].second>=1ll*-i*(q[front+1].first-q[front].first))front++;
		dp[f][i]=max(dp[f][i],q[front].second+1ll*i*q[front].first);
	}
}
void work(int f)
{
	int front=0,rear=0;
	que[0]=0;
	for(int i=1;i<=n;i++)
	{
		int pos=query(front,rear,b[i]);
		dp[f][i]=max(dp[f][i],sum[que[pos]]+1ll*b[i]*(i-que[pos]));
		while(front<rear&&(sum[que[rear]]-sum[que[rear-1]])*1ll*(i-que[rear])<1ll*(que[rear]-que[rear-1])*(sum[i]-sum[que[rear]]))rear--;
		que[++rear]=i;
	}
	CDQ(0,n,f);
}
int main()
{
	init();
	work(0);
	reverse();
	work(1);
	reverse();
	for(int i=1,j=n;i<=n/2;i++,j--)swap(dp[1][i],dp[1][j]);
	ll ans=sum[n],mx=0;
	for(int i=1;i<=n;i++)
	{
		ans=max(ans,dp[1][i]+sum[i-1]+mx);
		mx=max(mx,dp[0][i]-sum[i]);
	}
	printf("%I64d\n",ans);
}