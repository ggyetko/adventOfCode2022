10 t1=0:t2=0:t3=0
20 tt=0
30 cc$ = "": input cc$
40 if cc$="" then gosub 100: goto 20
45 if cc$="x" then gosub 100: goto 200
50 tt = tt + val(cc$)
60 goto 30
100 :
110 if tt>t1 then t3=t2:t2=t1:t1=tt:return
120 if tt>t2 then t3=t2:t2=tt:return
130 if tt>t3 then t3=tt
140 return
150 :
200 print t1,t2,t3
210 print "total";t1+t2+t3