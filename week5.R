library(ggplot2)

df <- read.csv("~/python/df.csv")
ch <- read.csv("~/python/ch.csv")

df$xstd=df$x-mean(df$x)
df$ystd=df$y-mean(df$y)
xmean=mean(df$x)
ymean=mean(df$y)

xrange=seq(-5000,6000,by=100)
yrange=seq(-4500,6000,by=100)
xlen=length(xrange)
ylen=length(yrange)

distance <- function(x,y,x1,y1) {
  return(sqrt((x-x1)^2+(y-y1)^2))
}

d=matrix(0,nrow=xlen,ncol=ylen)

data <- expand.grid(X=xrange, Y=yrange)

for(x in 1:ylen)
  for(y in 1:xlen) {
    for(i in 1:length(df$zip))
      d[y,x]=d[y,x]+distance(df$xstd[i],df$ystd[i],yrange[x],xrange[y])^0.1*df$population[i]*10^-6
    d[y,x]=d[y,x]^3*100
  }

data$Z=matrix(unlist(d),nrow=xlen*ylen)

row=c(11,14,9,37,43,47,49,58,65,82,83,110) 
col=c(18,48,82,51,29,1,101,62,36,38,73,7)

ch$xstd=ch$x-mean(ch$x)
ch$ystd=ch$y-mean(ch$y)

empty=data.frame(rep(0,dim(pp)[1]))

potential_points=data.frame('Location'=LETTERS[1:length(row)])
potential_points$xstd=round(xrange[row],2)
potential_points$ystd=round(yrange[col],2)
potential_points$x=potential_points$xstd+xmean
potential_points$y=potential_points$ystd+ymean

pp=potential_points
pp$row=row
pp$col=col
pp=pp[order(pp$row,decreasing = FALSE),]

pp$dot=rep(0,dim(c)[1])
for(i in 1:dim(pp)[1])
  for(j in 1:length(ch$Name))
    pp$dot[i]=pp$dot[i]+distance(ch$x[j],ch$y[j],pp$x[i],pp$y[i])

p=ggplot(data, aes(X, Y, z=Z)) + geom_tile(aes(fill = Z))+ 
  theme_bw()+ 
  scale_fill_gradient(high="black", low="white")+
  geom_point(data=df,aes(xstd,ystd),cex=3,shape=19,color='red',inherit.aes = FALSE)+
  geom_point(data=empty,aes(xrange[pp$row],yrange[pp$col]),inherit.aes = FALSE,
             shape=LETTERS[1:dim(pp)[1]],color='blue',cex=3)+
  geom_point(data=ch,aes(xstd,ystd),inherit.aes = FALSE,
             shape=17,color='yellow',cex=3)

write.csv(pp,'~/python/potential_points.csv',row.names = FALSE)
write.csv(t(d),'~/python/d.csv',row.names=FALSE)

plot(p)