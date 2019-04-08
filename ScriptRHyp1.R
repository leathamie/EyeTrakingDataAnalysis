dataK <- read.table(file.choose(),header=T)

#Shapiro tests pour choisir le test à faire
shapiro.test(dataK$AFS)
shapiro.test(dataK$ANS)
shapiro.test(dataK$DIS)
shapiro.test(dataK$HAS)
shapiro.test(dataK$NES)
shapiro.test(dataK$SAS)
shapiro.test(dataK$SUS)

# Représentation graphique
mg = sapply(dataK,mean)
sem = sapply(dataK, sd)
x= barplot(mg)

arrows(x[1], mg[1]-sem[1],x[1],mg[1]+sem[1], angle=90, code=3)
arrows(x[2], mg[2]-sem[2],x[2],mg[2]+sem[2], angle=90, code=3)
arrows(x[3], mg[3]-sem[3],x[3],mg[3]+sem[3], angle=90, code=3)
arrows(x[4], mg[4]-sem[4],x[4],mg[4]+sem[4], angle=90, code=3)
arrows(x[4], mg[4]-sem[4],x[4],mg[4]+sem[4], angle=90, code=3)
arrows(x[5], mg[5]-sem[5],x[5],mg[5]+sem[5], angle=90, code=3)
arrows(x[6], mg[6]-sem[6],x[6],mg[6]+sem[6], angle=90, code=3)
arrows(x[7], mg[7]-sem[7],x[7],mg[7]+sem[7], angle=90, code=3)

#si shapiro rejetté
kruskal.test(dataK)

#si shapiro accepté
anova(dataK)
