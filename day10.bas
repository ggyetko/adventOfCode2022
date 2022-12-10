10 ck = 0: rem clock cycle
20 sp = 0: rem sum of products
30 rx = 1: rem register x
40
100 input a$
110 if left$(a$,1) = "x" then goto 200
120 if left$(a$,1) = "n" then gosub 1000: goto 100
130 gosub 1000
140 gosub 1000
150 dx=val(mid$(a$,5,5))
160 rx=rx+dx
170 goto 100
180 :
200 print "part 1:";sp
210 end
220 :
1000 cc=ck
1010 if cc<40 then 1030
1020 cc=cc-40:goto 1010
1030 if cc=19 then sp=sp+rx*(ck+1):print ck,rx
1040 ck=ck+1
1050 return


