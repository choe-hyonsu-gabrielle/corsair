# corsair
A lightweight concordance view for NIKL "Modu" Corpora.


### Requirements
```commandline
$ pip install tqdm openpyxl
```


### Run
```NXMP1902008040.json```, ```SXMP1902008031.json``` 파일이 ```./corpora``` 폴더에 들어 있을 때, 아래와 같이 실행합니다.
```commandline
$ python corsair.py
```
또는 원하는 directory를 실행 시 인자로 넘겨 줍니다.
```commandline
$ python corsair.py --dir ./YOUR_AWESOME_DATA/*.json --window_size 5 --map_window_size 2
```


### Commands
```
[-raw/-rawx/-pos/-posx] [primary expression] (secondary expression) or '-quit'
```


#### 원시 텍스트를 기준으로 Unigram 검색
```[Corsair] >>> -raw 나는```
```commandline
...
1766  ./SXMP1902008031.json    SDRW1800000006.156     15 나는거야. (나/VV+는/ETM+거/NNB+이/VCP+야/EF+./SF)        ⋯ 어머니 얼굴 보는데 눈물이 내가 나는거야.                          ⋯ 눈물/NNG+이/JKS 내/NP+가/JKS 나/VV+는/ETM+거/NNB+이/VCP+야/EF+./SF                          
1767  ./SXMP1902008031.json    SDRW1800000006.1416    6  나는거야. (나/VV+는/ETM+거/NNB+이/VCP+야/EF+./SF)           요새 얼굴에 땀이 막 미친듯이 나는거야.                          ⋯ 막/MAG 미치/VV+ㄴ/ETM+듯이/NNB 나/VV+는/ETM+거/NNB+이/VCP+야/EF+./SF                          
1768  ./SXMP1902008031.json    SDRW1800000006.173     4  눈물나는지 (눈물/NNG+나/VV+는지/EC)                     아 근데 왜 눈물나는지 잘 모르겠지 않냐 나는 좀.                     ⋯ 근데/MAJ 왜/MAG 눈물/NNG+나/VV+는지/EC 잘/MAG 모르/VV+겠/EP+지/EC ⋯  
1769  ./SXMP1902008031.json    SDRW1800000006.1333    2  아시아나는 (아시아나/NNP+는/JX)                       대한항공 아시아나는 진짜 타본 적이 없어.                              대한항공/NNP 아시아나/NNP+는/JX 진짜/MAG 타/VV+아/EC+보/VX+ㄴ/ETM ⋯
1770  ./SXMP1902008031.json    SDRW1800000006.1420    10 안나는거야. (안/MAG+나/VV+는/ETM+거/NNB+이/VCP+야/EF+./SF)      ⋯ 바르고 자면은 다음날 얼굴에선 땀이 안나는거야.                          ⋯ 얼굴/NNG+에서/JKB+ㄴ/JX 땀/NNG+이/JKS 안/MAG+나/VV+는/ETM+거/NNB+이/VCP+야/EF+./SF                          
1771  ./SXMP1902008031.json    SDRW1800000006.2167    5  생각나는거야. (생각나/VV+는/ETM+거/NNB+이/VCP+야/EF+./SF)        name4랑 했던 퍼스널컬러가 자꾸 생각나는거야.                          ⋯ 퍼스널/NNG+컬러/NNG+가/JKS 자꾸/MAG 생각나/VV+는/ETM+거/NNB+이/VCP+야/EF+./SF                          
1772  ./SXMP1902008031.json    SDRW1800000011.413     11 나는구나. (나/VV+는구나/EF+./SF)     ⋯ 무료쿠폰 얘기를 들으니까 완전 생각이 나는구나.                              ⋯ 완전/NNG 생각/NNG+이/JKS 나/VV+는구나/EF+./SF                          
1773  ./SXMP1902008031.json    SDRW1800000015.261     2  타고나는 (타고나/VV+는/ETM)                          네 타고나는 그거 있어요.                                       네/IC 타고나/VV+는/ETM 그거/NP 있/VA+어요/EF+./SF    
1774  ./SXMP1902008031.json    SDRW1800000020.62      3  열나는 (열나/VV+는/ETM)                       그 안에 열나는 건                                그/MMD 안/NNG+에/JKB 열나/VV+는/ETM 거/NNB+ㄴ/JX               
1775  ./SXMP1902008031.json    SDRW1800000020.2442    3  늘어나는데 (늘어나/VV+는데/EC)                    왜냐면 수명은 늘어나는데                                왜냐면/MAG 수명/NNG+은/JX 늘어나/VV+는데/EC                          
[Corsair] Query: 나는 (1775 results)
[Corsair] Top-10 frequency: [('나는', 1233), ('하나는', 184), ('나타나는', 42), ('만나는', 34), ('일어나는', 31), ('나는데', 27), ('끝나는', 24), ('늘어나는', 14), ('나는.', 10), ('생각나는', 9)] ⋯
```

#### 원시 텍스트를 기준으로 Bigram 검색
```[Corsair] >>> -raw 는 게```
```commandline
...
1646  ./SXMP1902008031.json    SDRW1800000020.1496    3  중독이라는 게 (중독/NNG+이/VCP+라는/ETM 거/NNB+이/JKS)                      근데 그게 중독이라는 게 있어 갖고                           근데/MAJ 그거/NP+이/JKS 중독/NNG+이/VCP+라는/ETM 거/NNB+이/JKS 있/VA+어/EC 갖/VX+고/EC      
1647  ./SXMP1902008031.json    SDRW1800000020.2267    2  믿는 게 (믿/VV+는/ETM 거/NNB+이/JKC)                          못 믿는 게 아니라                                          못/MAG 믿/VV+는/ETM 거/NNB+이/JKC 아니/VCN+라/EC              
1648  ./SXMP1902008031.json    SDRW1800000020.2639    2  보약이라는 게 (보약/NNG+이/VCP+라는/ETM 거/NNB+이/JKS)                         잠이 보약이라는 게 맞아 근데                                  잠/NNG+이/JKS 보약/NNG+이/VCP+라는/ETM 거/NNB+이/JKS 맞/VV+아/EF 근데/MAJ         
1649  ./SXMP1902008031.json    SDRW1800000020.2687    2  공유하는 게 (공유/NNG+하/XSV+는/ETM 거/NNB+이/JKC)                       부부하고 공유하는 게 아니잖아.                                부부/NNG+하고/JKB 공유/NNG+하/XSV+는/ETM 거/NNB+이/JKC 아니/VCN+잖아/EF+./SF        
1650  ./SXMP1902008031.json    SDRW1800000020.2815    2  지내는 게 (지내/VV+는/ETM 거/NNB+이/JKC)                      올해까지만 지내는 게 아니라                              올해/NNG+까지/JX+만/JX 지내/VV+는/ETM 거/NNB+이/JKC 아니/VCN+라/EC              
1651  ./SXMP1902008031.json    SDRW1800000020.2839    3  사드리는 게 (사/VV+아/EC+드리/VX+는/ETM 거/NNB+이/JKS)                      맛있는 거 사드리는 게                                  맛있/VA+는/ETM 거/NNB 사/VV+아/EC+드리/VX+는/ETM 거/NNB+이/JKS                          
1652  ./SXMP1902008031.json    SDRW1800000030.272     10 있대는 게 (있/VA+대는/ETM 거/NNB+이/JKS)          ⋯ 그렇게 걔가 연주를 끝낼 수 있대는 게 참 대단한 거 같애                     ⋯ 끝내/VV+ㄹ/ETM 수/NNB 있/VA+대는/ETM 거/NNB+이/JKS 참/MAG 대단하/VA+ㄴ/ETM ⋯     
1653  ./SXMP1902008031.json    SDRW1800000030.574     5  입는 게 (입/VV+는/ETM 거/NNB+이/JKS)               그냥 약간 젊어 보이게 입는 게 좋지 이제 나이도 먹고 하니까            ⋯ 젊/VA+어/EC 보이/VV+게/EC 입/VV+는/ETM 거/NNB+이/JKS 좋/VA+지/EF 이제/MAG ⋯       
1654  ./SXMP1902008031.json    SDRW1800000030.626     6  기도하는 게 (기도/NNG+하/XSV+는/ETM 거/NNB+이/JKS)           우리 애들이 니네가 내가 항상 기도하는 게 사회에 봉사하면서 평생 살게 해달라고 ⋯         ⋯ 내/NP+가/JKS 항상/MAG 기도/NNG+하/XSV+는/ETM 거/NNB+이/JKS 사회/NNG+에/JKB 봉사/NNG+하/XSV+면서/EC ⋯
1655  ./SXMP1902008031.json    SDRW1800000030.963     2  구경하는 게 (구경/NNG+하/XSV+는/ETM 거/NNB+이/JKS)                         많이 구경하는 게 좋지 해가지고                                     많이/MAG 구경/NNG+하/XSV+는/ETM 거/NNB+이/JKS 좋/VA+지/EF 하/VV+아/EC+가지/VX+고/EC
[Corsair] Query: 는 게 (1655 results)
[Corsair] Top-10 frequency: [('하는 게', 193), ('있는 게', 113), ('되는 게', 50), ('가는 게', 31), ('넣는 게', 31), ('없는 게', 24), ('사는 게', 23), ('주는 게', 22), ('보는 게', 20), ('얘기하는 게', 17)] ⋯
```

#### 형태 분석 시퀀스를 기준으로 Bigram 정규식 검색
```[Corsair] >>> -pos ^학교.* .*/V```
```commandline
...
241   ./SXMP1902008031.json    SDRW1800000009.875     2  학교/NNG 가/VV+던가/EF+?/SF (학교 가던가?)                  타/VV+고/EC 학교/NNG 가/VV+던가/EF+?/SF                                                 타고 학교 가던가?                          
242   ./SXMP1902008031.json    SDRW1800000009.991     8  학교/NNG+를/JKO 가/VV+다가/EC (학교를 가다가)  ⋯ 다행히/MAG 그/IC 원래/MAG 선유도/NNP 역/NNG+에서/JKB 학교/NNG+를/JKO 가/VV+다가/EC                                          ⋯ 선유도 역에서 학교를 가다가                          
243   ./SXMP1902008031.json    SDRW1800000009.1090    5  학교/NNG+까지/JX 걸어가/VV+는/ETM (학교까지 걸어가는)  학/NA 그/IC 역/NNG+에서/JKB 내리/VV+어서/EC 학교/NNG+까지/JX 걸어가/VV+는/ETM 것/NNB+도/JX 진짜/MAG 힘들/VA+어/EF+./SF                ⋯ 역에서 내려서 학교까지 걸어가는 것도 진짜 ⋯                  
244   ./SXMP1902008031.json    SDRW1800000009.1378    2  학교/NNG+에/JKB 이쁘/VA+ㄴ/ETM (학교에 이쁜)                 너/NP+네/XSN 학교/NNG+에/JKB 이쁘/VA+ㄴ/ETM 교수/NNG+님/XSN 너/NP+가/JKS 막/MAG 사진/NNG 찍/VV+어서/EC ⋯                       너네 학교에 이쁜 교수님 너가 ⋯                 
245   ./SXMP1902008031.json    SDRW1800000015.234     6  학교/NNG 들어가/VV+ㄹ/ETM (학교 들어갈)  꼭/MAG 그거/NP+이/JKS 이제/IC 이거/NP+이/JKS 뭐/IC 학교/NNG 들어가/VV+ㄹ/ETM 때/NNG                                       ⋯ 이게 뭐 학교 들어갈 때                        
246   ./SXMP1902008031.json    SDRW1800000015.773     2  학교/NNG+는/JX 많/VA+아요/EF+./SF (학교는 많아요.)               주변/NNG+에/JKB 학교/NNG+는/JX 많/VA+아요/EF+./SF                                                주변에 학교는 많아요.                          
247   ./SXMP1902008031.json    SDRW1800000015.775     1  학교/NNG 많/VA+고/EC (학교 많고)                            학교/NNG 많/VA+고/EC 장위동/NNP 같/VA+은/ETM 경우/NNG+는/JX 뭐/IC                          학교 많고 장위동 같은 ⋯                 
248   ./SXMP1902008031.json    SDRW1800000015.1202    1  학교/NNG+도/JX 좋/VA+고/EC (학교도 좋고)                            학교/NNG+도/JX 좋/VA+고/EC 그니까/MAJ 이거/NP+를/JKO 부모/NNG+님/XSN+한테/JKB 말씀/NNG+을/JKO 못/MAG ⋯                          학교도 좋고 그니까 이거를 ⋯                
249   ./SXMP1902008031.json    SDRW1800000020.31      1  학교/NNG+에서/JKB+도/JX 그렇/VA+고/EC (학교에서도 그렇고)                            학교/NNG+에서/JKB+도/JX 그렇/VA+고/EC                                                    학교에서도 그렇고                          
250   ./SXMP1902008031.json    SDRW1800000030.1154    4  학교/NNG 다니/VV+면서/EC+도/JX (학교 다니면서도)  거기/NP+에/JKB 내/NP+가/JKS 좀/MAG 학교/NNG 다니/VV+면서/EC+도/JX 합창단/NNG 돈/NNG+이/JKS 나오/VV+니까/EC 빠지/VV+어/EC 있/VX+었/EP+잖아/EF                   ⋯ 내가 좀 학교 다니면서도 합창단 돈이 ⋯                 
[Corsair] Query: ^학교.* .*/V (250 results)
[Corsair] Top-10 frequency: [('학교/NNG 다니/VV+ㄹ/ETM', 12), ('학교/NNG 가/VV+았/EP+다/EC', 5), ('학교/NNG 가/VV+고/EC', 4), ('학교/NNG+에/JKB 대하/VV+ㄴ/ETM', 3), ('학교/NNG 같/VA+은/ETM', 3), ('학교/NNG 가/VV+ㄹ/ETM', 3), ('학교/NNG 가/VV+아서/EC', 3), ('학교/NNG 가/VV+는/ETM', 3), ('학교/NNG+에/JKB 가/VV+ㄹ/ETM', 2), ('학교/NNG+에/JKB 가/VV+고/EC', 2)] ⋯
```

#### 형태 분석 시퀀스를 기준으로 Bigram 정규식 검색 결과를 Excel 파일로 저장 
```[Corsair] >>> -posx ^회사.* .*/MAG```
```commandline
27    ./SXMP1902008031.json    SBRW1800000032.499     3  회사/NNG+들/XSN+이/JKS 아직/MAG+까지/JX (회사들이 아직까지)  노동조합/NNG+을/JKO 싫어하/VV+는/ETM 회사/NNG+들/XSN+이/JKS 아직/MAG+까지/JX 많이/MAG 있/VA+습니다/EF                      노동조합을 싫어하는 회사들이 아직까지 많이 있습니다                  
28    ./SXMP1902008031.json    SBRW1800000032.543     2  회사/NNG+에서/JKB 정말/MAG (회사에서 정말)                     또는/MAG 회사/NNG+에서/JKB 정말/MAG 꼴찌/NNG+에서/JKB 오/NR 프로/NNB+이/VCP+ㄴ/ETM 애/NNG+들/XSN 정도/NNG+로/JKB ⋯                       또는 회사에서 정말 꼴찌에서 오 ⋯                 
29    ./SXMP1902008031.json    SBRW1800000032.583     6  회사/NNG+들/XSN+은/JX 좀/MAG (회사들은 좀)  최고/NNG 높/VA+은/ETM 임금/NNG+이나/JC 근로/NNG+조건/NNG+을/JKO 적용/NNG+하/XSV+는/ETM 회사/NNG+들/XSN+은/JX 좀/MAG                                       ⋯ 근로조건을 적용하는 회사들은 좀                          
30    ./SXMP1902008031.json    SBRW1800000032.586     3  회사/NNG+는/JX 좀/MAG (회사는 좀)          저런/MMD 좋/VA+은/ETM 회사/NNG+는/JX 좀/MAG 칭찬/NNG+도/JX 하/VV+아/EC 주/VX+고/EC 지원/NNG+하/XSV+아/EC+주/VX+고/EC                    저런 좋은 회사는 좀 칭찬도 해 ⋯                  
31    ./SXMP1902008031.json    SDRW1800000006.1570    5  회사/NNG+다니/VV+면/EC 보통/MAG (회사다니면 보통)  근데/MAJ 자기/NP+도/JX 지금/MAG 원래/MAG 회사/NNG+다니/VV+면/EC 보통/MAG 하/VV+라고/EC 나오/VV+잖아/EF+./SF                  ⋯ 지금 원래 회사다니면 보통 하라고 나오잖아.                
32    ./SXMP1902008031.json    SDRW1800000007.244     9  회사/NNG+들/XSN+이/JKS 되게/MAG (회사들이 되게)  ⋯ 지금/MAG 나/NP 공고/NNG+에/JKB 보/VV+니까/EC 뽑/VV+는/ETM 회사/NNG+들/XSN+이/JKS 되게/MAG 많/VA+아/EF                                 ⋯ 보니까 뽑는 회사들이 되게 많아                       
33    ./SXMP1902008031.json    SDRW1800000007.980     4  회사/NNG 다/MAG (회사 다)  딸/NNG 하나/NR+이/VCP+ㄴ데/EC 그/MMD 회사/NNG 다/MAG 사위/NNG+한테/JKB 다/MAG 주/VV+어야/EC 되/VV+어/EF                  ⋯ 하난데 그 회사 다 사위한테 다 ⋯                 
34    ./SXMP1902008031.json    SDRW1800000009.648     2  회사원/NNG+들/XSN+도/JX 엄청/MAG (회사원들도 엄청)                    그래서/MAJ 회사원/NNG+들/XSN+도/JX 엄청/MAG 많/VA+잖아/EF+./SF                                그래서 회사원들도 엄청 많잖아.                     
35    ./SXMP1902008031.json    SDRW1800000018.885     2  회사/NNG+도/JX 안/MAG (회사도 안)                 내/NP+가/JKS 회사/NNG+도/JX 안/MAG 다니/VV+고/EC 집/NNG+에서/JKB                         내가 회사도 안 다니고 집에서                  
36    ./SXMP1902008031.json    SDRW1800000030.454     6  회사/NNG+에서/JKB 막/MAG (회사에서 막)  회사/NNG 일/NNG+만/JX 바쁘/VA+고/EC 그냥/MAG 항상/MAG 회사/NNG+에서/JKB 막/MAG 야근/NNG+하/XSV+고/EC 막/MAG 이렇/VA+게/EC 오/VV+니까/EC 좀/MAG ⋯                  ⋯ 그냥 항상 회사에서 막 야근하고 막 ⋯                 
[Corsair] Query: ^회사.* .*/MAG (36 results)
[Corsair] Top-10 frequency: [('회사/NNG+를/JKO 다/MAG', 1), ('회사/NNG+를/JKO 그만/MAG', 1), ('회사/NNG+를/JKO 안/MAG', 1), ('회사/NNG+에/JKB 다/MAG', 1), ('회사/NNG+에/JKB 지금/MAG', 1), ('회사/NNG+에서/JKB 너무/MAG', 1), ('회사/NNG 좀/MAG', 1), ('회사/NNG+와/JKB 함께/MAG', 1), ('회사/NNG+도/JX 좀/MAG', 1), ('회사/NNG 또는/MAG', 1)] ⋯
[Corsair] Saved 36 results to file: "corsair_export-2022-06-04-19.16.27.xlsx"
```