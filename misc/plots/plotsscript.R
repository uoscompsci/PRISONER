library(ggplot2)
library(scales)
#box_cols = c("#635855","#CF6148")
box_cols = c(rgb(0.471,0.722,0.098),rgb(0.098,0.639,0.722))
font_size <- 12


# START descriptive plots
dev.new(width=7,height=5)
results <- read.table("Results_Complete.txt",header=T)
# differences between two groups
info_agg <- ddply(results,c("ParticipantID","GroupID"),function(df) return(c(AVERAGE=mean(df$Response), MEDIAN=median(df$Response),SD=sd(df$Response),SE=sqrt(var(df$Response)/length(df$Response)))))
boxplot(info_agg$AVERAGE~info_agg$GroupID)
Group <- factor(info_agg$GroupID, labels=c("T3","LocShare"))
p <- ggplot(info_agg,aes(Group,AVERAGE), label)
p + geom_boxplot(aes(fill=Group)) +
scale_y_continuous("Proportion of data shared (%)",limits = c(0, 1),labels=percent_format()) +
scale_x_discrete("Participant Group") +
scale_fill_manual("",values=box_cols) +
theme_bw(base_size=font_size) +	
coord_fixed() +
coord_equal(ratio=2) +
opts(axis.text.x=theme_text(size=font_size),axis.text.y=theme_text(size=font_size),legend.key = theme_rect(col = 0),legend.text=theme_text(size=font_size),axis.title.x=theme_text(vjust=0,size=font_size,face="bold"),axis.title.y=theme_text(hjust=0.5,vjust=0.15,angle=90,size=font_size,face="bold"))
ggsave(file="partgroup.eps")

# differences between information types, sub-divided by participant group
dev.new(width=10,height=3)
info_agg <- ddply(results,c("ParticipantID","GroupID","InfoType"),function(df) return(c(AVERAGE=mean(df$Response), MEDIAN=median(df$Response),SD=sd(df$Response),SE=sqrt(var(df$Response)/length(df$Response)))))
Group <- factor(info_agg$GroupID, labels=c("T3","LocShare"))
p <- ggplot(info_agg,aes(InfoType,AVERAGE), label)
p + geom_boxplot(aes(fill=Group)) +
scale_y_continuous("Proportion of data shared (%)",limits = c(0, 1),labels=percent_format()) +
scale_x_discrete("Information type") +
scale_fill_manual("",values=box_cols) +
theme_bw(base_size=font_size) +	
coord_equal(ratio=2) +
opts(axis.text.x=theme_text(size=font_size),axis.text.y=theme_text(size=font_size),legend.key = theme_rect(col = 0),legend.text=theme_text(size=font_size),axis.title.x=theme_text(vjust=0,size=font_size,face="bold"),axis.title.y=theme_text(hjust=0.5,vjust=0.15,angle=90,size=font_size,face="bold"))
ggsave(file="infotype.eps")

# differences between privacy settings, sub-divided by participant group
dev.new(width=10,height=5)
results <- read.table("Results_Privacy_Reduced.txt",header=T)
info_agg <- ddply(results,c("ParticipantID","GroupID","PrivacySetting"),function(df) return(c(AVERAGE=mean(df$Response), MEDIAN=median(df$Response),SD=sd(df$Response),SE=sqrt(var(df$Response)/length(df$Response)))))
Group <- factor(info_agg$GroupID, labels=c("T3","LocShare"))
p <- ggplot(info_agg,aes(PrivacySetting,AVERAGE), label)
p + geom_boxplot(aes(fill=Group)) +
scale_y_continuous("Proportion of data shared (%)",limits = c(0, 1),labels=percent_format()) +
scale_x_discrete("Privacy setting",limits=c("EVERYONE","FRIENDS-OF-FRIENDS","FRIENDS","CUSTOM"),labels=c("Everyone","Friends of friends","Friends","Custom")) +
scale_fill_manual("",values=box_cols) +
theme_bw(base_size=font_size) +
coord_equal(ratio=2) +
opts(axis.text.x=theme_text(size=font_size),axis.text.y=theme_text(size=font_size),legend.key = theme_rect(col = 0),legend.text=theme_text(size=font_size),axis.title.x=theme_text(vjust=0,size=font_size,face="bold"),axis.title.y=theme_text(hjust=0.5,vjust=0.15,angle=90,size=font_size,face="bold"))
ggsave(file="privsetting.eps")