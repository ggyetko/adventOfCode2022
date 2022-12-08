10 dim gg%(100,100)
15 y=1:x=1
20 get a$
21 if a$ = "" then 20
23 if a$ = "x" then 70
30 if asc(a$) = 13 then 60
40 gg%(x,y)= val(a$)
50 x=x+1: goto 20
60 print"lines:";y:mx=x-1:x=1:y=y+1:goto
 20
70 my = y - 1
75 printmx;"x";my:goto 155
80 for y = 1 to my
90 for x = 1 to mx
100 printgg%(x,y);
110 next x
120 print
130 next y
150 :
160 for ty = 1 to my
170 for tx = 1 to mx
180 tv = 0
190 vv = 1
192 hh = gg%(tx,ty)
195 if ty = 1 then goto 230
200 for y = ty-1 to 1 step -1
210 if gg%(tx,y) >= hh then vv = 0
220 next y
230 if vv = 1 then tv = 1:goto 395
240 vv = 1
245 if ty= my then  goto 280
250 for y = ty+1 to my
260 if gg%(tx,y) >= hh then vv = 0
270 next y
280 if vv = 1 then tv = 1:goto 395
290 vv = 1
295 if tx= 1 then goto 330
300 for x = tx-1 to 1 step -1
290 vv = 1
295 if tx= 1 then goto 330
300 for x = tx-1 to 1 step -1
310 if gg%(x,ty) >= hh then vv = 0
320 next x
330 if vv = 1 then tv = 1:goto 395
340 vv = 1
345 if tx= mx then  goto 380
350 for x = tx+1 to mx
360 if gg%(x,ty) >= hh then vv = 0
370 next x
380 if vv = 1 then tv = 1
390 :
395 if tv = 1 then vc = vc + 1
400 next tx
405 print "line done:";ty
410 next ty
420 :
430 print vc


