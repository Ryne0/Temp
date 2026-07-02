# I欄電子元件分類整理

資料來源：由照片辨識出的 Excel I 欄料號，並在旁邊補上「分類」與「SMT / DIP」。

> 注意：分類與封裝判斷為初步整理；備註欄含「建議核對」者，請再以原始 BOM、實物封裝或供應商 datasheet 確認。

## 統計摘要

### 分類大類

| 分類大類 | 數量 |
|---|---:|
| 電阻 | 30 |
| 電容 | 24 |
| 連接器 | 7 |
| 二極體 | 7 |
| IC | 7 |
| 電晶體 | 7 |
| 電感 | 4 |
| 保險絲 | 1 |
| 濾波器 | 1 |

### SMT / DIP

| SMT / DIP | 數量 |
|---|---:|
| SMT | 81 |
| DIP/TH | 7 |

## 需特別核對項目

| 序號 | I欄內容 | 分類 | SMT / DIP | 備註/核對點 | 來源 |
|---:|---|---|---|---|---|
| 7 | `GYB1V151MCQ1GS` | 電容 / 鋁聚合物或混合電容 | SMT | Nichicon GYB，150uF 35V，Aluminum/Polymer SMD；建議核對實際系列 | [來源](<https://www.digikey.tw/zh/products/detail/nichicon/GYB1V151MCQ1GS/9487123>) |
| 15 | `ADCR-X02R7SB105PT` | 電容 / 超級電容 EDLC | DIP/TH | Abracon 1F 2.7V supercapacitor；照片看起來為徑向/插件，請核對實物腳位 | [來源](<https://www.digikey.in/en/products/detail/abracon-llc/ADCR-X02R7SB105PT/25660740>) |
| 36 | `LMR51450FSQDRRRQ1` | IC / DC-DC Buck切換穩壓器 | SMT | TI LMR51450-Q1 5A buck regulator IC，12-WSON；照片字元建議核對 | [來源](<https://www.digikey.tw/zh/products/detail/texas-instruments/LMR51450FSQDRRRQ1/25318409>) |
| 37 | `LMR51420YDDCR,PLMR51420XDDCT` | IC / DC-DC Buck切換穩壓器 | SMT | TI LMR51420 2A synchronous buck；此格似乎合併兩個料號，請拆開核對 | [來源](<https://www.digikey.com.au/en/products/detail/texas-instruments/LMR51420YDDCR/16705132>) |
| 43 | `SSQ-112-01-L-D` | 連接器 / Samtec 排針座/母座 | DIP/TH | Samtec SSQ系列，依SSQ-110同系列推定 through-hole；請核對12位版本 | [來源](<https://www.samtec.com/products/ssq-110-01-l-d-001>) |
| 53 | `NX7002BKWX` | 電晶體 / N-Channel MOSFET | SMT | Nexperia/NX7002 60V N-channel MOSFET，SOT-23；料號尾碼請核對 | [來源](<https://octopart.com/zh/datasheet/nexperia/NX7002BKWX>) |

## 完整明細

| 序號 | I欄內容 | 分類 | SMT / DIP | 備註/核對點 | 來源 |
|---:|---|---|---|---|---|
| 1 | `CGA5L2C0G1H104J160AA` | 電容 / MLCC陶瓷電容 | SMT | TDK CGA/C系列，SMD MLCC；依料號與照片廠商判斷 | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 2 | `CC0603JRX7R9BB104` | 電容 / MLCC陶瓷電容 | SMT | Yageo CC0603，0.1uF 50V X7R 0603 MLCC | [來源](<https://yageogroup.com/download/specsheet/CC0603JRX7R9BB104>) |
| 3 | `C1005X7R1E103K050BB` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005系列，SMD MLCC | [來源](<https://datasheet.octopart.com/C1005X7R1E223K-TDK-datasheet-57437.pdf>) |
| 4 | `CGA3E1X7R1V474K080AC` | 電容 / MLCC陶瓷電容 | SMT | TDK CGA車規MLCC系列 | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 5 | `C1005X7R1C104K050BC` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 6 | `C3225X7R1C226M250AC` | 電容 / MLCC陶瓷電容 | SMT | TDK C3225系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 7 | `GYB1V151MCQ1GS` | 電容 / 鋁聚合物或混合電容 | SMT | Nichicon GYB，150uF 35V，Aluminum/Polymer SMD；建議核對實際系列 | [來源](<https://www.digikey.tw/zh/products/detail/nichicon/GYB1V151MCQ1GS/9487123>) |
| 8 | `C1005C0G1H101J050BA` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005 C0G系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 9 | `C3225X7R1H475K250AB` | 電容 / MLCC陶瓷電容 | SMT | TDK C3225系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 10 | `C1005X7R1H104K050BB` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 11 | `C2012X7R1V475K125AC` | 電容 / MLCC陶瓷電容 | SMT | TDK C2012系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 12 | `C1005C0G1H102J050BA` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005 C0G系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 13 | `C1005C0G1H101J050BA` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005 C0G系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 14 | `UUD1H151MNL1GS` | 電容 / 鋁電解電容 | SMT | Nichicon UUD，150uF 50V，Aluminum Electrolytic Capacitors - SMD | [來源](<https://www.ttieurope.com/content/ttieurope/en/apps/part-detail.html?mfgShortname=NIC&partsNumber=UUD1H151MNL1GS>) |
| 15 | `ADCR-X02R7SB105PT` | 電容 / 超級電容 EDLC | DIP/TH | Abracon 1F 2.7V supercapacitor；照片看起來為徑向/插件，請核對實物腳位 | [來源](<https://www.digikey.in/en/products/detail/abracon-llc/ADCR-X02R7SB105PT/25660740>) |
| 16 | `C2012X7R0J106K125AB` | 電容 / MLCC陶瓷電容 | SMT | TDK C2012系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 17 | `C1005X7S1A474K050BC` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 18 | `C1005X7R1E223K050BB` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005系列，SMD MLCC | [來源](<https://datasheet.octopart.com/C1005X7R1E223K-TDK-datasheet-57437.pdf>) |
| 19 | `C1005C0G1H100D050BA` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005 C0G系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 20 | `C1005C0G1H471J050BA` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005 C0G系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 21 | `C1005X7R1H222K050BA` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 22 | `CC0603JRX7R9BB104` | 電容 / MLCC陶瓷電容 | SMT | Yageo CC0603，0.1uF 50V X7R 0603 MLCC | [來源](<https://yageogroup.com/download/specsheet/CC0603JRX7R9BB104>) |
| 23 | `C1005X7R1E103K050BB` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005系列，SMD MLCC | [來源](<https://datasheet.octopart.com/C1005X7R1E223K-TDK-datasheet-57437.pdf>) |
| 24 | `C1005C0G1H220J050BA` | 電容 / MLCC陶瓷電容 | SMT | TDK C1005 C0G系列，SMD MLCC | [來源](<https://product.tdk.com/info/en/catalog/datasheets/mlcc_commercial_soft_en.pdf>) |
| 25 | `1053141208` | 連接器 / Molex Nano-Fit 板端排針 | DIP/TH | Molex 8P right-angle header, through-hole | [來源](<https://www.molex.com/en-us/products/part-detail/1053141208>) |
| 26 | `1053141212` | 連接器 / Molex Nano-Fit 板端排針 | DIP/TH | Molex 12P right-angle header, through-hole | [來源](<https://www.molex.com/en-us/products/part-detail/1053141212>) |
| 27 | `CLP-110-02-F-D` | 連接器 / Samtec 板對板母座 | SMT | Samtec CLP 20P socket/receptacle, SMD | [來源](<https://www.digikey.tw/zh/products/detail/samtec-inc/CLP-110-02-F-D/1109825>) |
| 28 | `SSQ-110-01-L-D` | 連接器 / Samtec 排針座/母座 | DIP/TH | Samtec SSQ 20P socket, through-hole | [來源](<https://www.digikey.in/en/products/detail/samtec-inc/SSQ-110-01-L-D/6693011>) |
| 29 | `BZX884B12L-HG3-08` | 二極體 / Zener 穩壓二極體 | SMT | Vishay BZX884L系列小訊號Zener，DFN SMD | [來源](<https://www.vishay.com/docs/86186/bzx884l-series.pdf>) |
| 30 | `V8P10-M3/86A` | 二極體 / Schottky整流二極體 | SMT | Vishay 100V 8A Schottky rectifier，TO-277A SMD | [來源](<https://www.digikey.tw/zh/products/detail/vishay-general-semiconductor-diodes-division/V8P10-M3-86A/2048214>) |
| 31 | `D33V0S1U2LP1608-7` | 二極體 / TVS瞬態抑制二極體 | SMT | Diodes Inc. TVS diode，U-DFN1608-2 SMD | [來源](<https://www.digikey.com.au/en/products/detail/diodes-incorporated/D33V0S1U2LP1608-7/10674165>) |
| 32 | `SMF12A-E3-18` | 二極體 / TVS瞬態抑制二極體 | SMT | Vishay SMF12A TVS diode，DO-219AB SMD | [來源](<https://www.digikey.ca/en/products/detail/vishay-general-semiconductor-diodes-division/SMF12A-E3-18/4872351>) |
| 33 | `RB068MM-60TFTR` | 二極體 / Schottky Barrier Diode | SMT | ROHM Schottky diode/rectifier，SOD-123FL/PMDU SMD | [來源](<https://www.mouser.com/ProductDetail/ROHM-Semiconductor/RB068MM-60TFTR>) |
| 34 | `TF16SN2.00TTD` | 保險絲 / Chip Fuse | SMT | KOA TF16SN chip current fuse | [來源](<https://www.koaspeer.com/pdfs/TF.pdf>) |
| 35 | `ACM1211-102-2PL-TL01` | 濾波器/電感 / 共模扼流圈 | SMT | TDK common mode choke/filter，2 line surface mount | [來源](<https://www.digikey.com/en/products/detail/tdk/ACM1211-102-2PL-TL01/765031>) |
| 36 | `LMR51450FSQDRRRQ1` | IC / DC-DC Buck切換穩壓器 | SMT | TI LMR51450-Q1 5A buck regulator IC，12-WSON；照片字元建議核對 | [來源](<https://www.digikey.tw/zh/products/detail/texas-instruments/LMR51450FSQDRRRQ1/25318409>) |
| 37 | `LMR51420YDDCR,PLMR51420XDDCT` | IC / DC-DC Buck切換穩壓器 | SMT | TI LMR51420 2A synchronous buck；此格似乎合併兩個料號，請拆開核對 | [來源](<https://www.digikey.com.au/en/products/detail/texas-instruments/LMR51420YDDCR/16705132>) |
| 38 | `MAX38888ATD+T` | IC / PMIC超級電容備援Buck-Boost | SMT | ADI/Maxim backup power reversible buck/boost regulator/controller，14-TDFN | [來源](<https://www.analog.com/en/products/max38888.html>) |
| 39 | `MAX40203AUK+T` | IC / Ideal Diode ORing/電源切換 | SMT | ADI/Maxim ideal diode current switch，SOT-23-5 | [來源](<https://www.analog.com/en/products/max40203.html>) |
| 40 | `LM25117PMHX/NOPB` | IC / DC-DC Buck控制器 | SMT | TI synchronous buck controller，20-HTSSOP | [來源](<https://www.digikey.com.au/en/products/detail/texas-instruments/LM25117PMHX-NOPB/2754367>) |
| 41 | `TLV7022DDFR` | IC / 比較器 Comparator | SMT | TI TLV7022 low-voltage comparator，TSOT-23-8；非TLV702 LDO | [來源](<https://www.digikey.co.uk/en/products/detail/texas-instruments/TLV7022DDFR/13213529>) |
| 42 | `TLV9062IDDFR` | IC / 運算放大器 Op Amp | SMT | TI TLV9062 dual op amp，TSOT-23-8 | [來源](<https://www.digikey.ca/en/products/detail/texas-instruments/TLV9062IDDFR/10715409>) |
| 43 | `SSQ-112-01-L-D` | 連接器 / Samtec 排針座/母座 | DIP/TH | Samtec SSQ系列，依SSQ-110同系列推定 through-hole；請核對12位版本 | [來源](<https://www.samtec.com/products/ssq-110-01-l-d-001>) |
| 44 | `CPG-01-TH-B` | 連接器 / Pogo Pin 彈簧針 | DIP/TH | Same Sky pogo pin/contact spring，through-hole | [來源](<https://www.digikey.com/en/products/detail/same-sky-formerly-cui-devices/CPG-01-TH-B/22259457>) |
| 45 | `178495-1` | 連接器 / TE電源板端Header | DIP/TH | TE Universal Power 2P right-angle PCB mount header，through-hole solder | [來源](<https://www.te.com/en/product-178495-1.html>) |
| 46 | `SPM6545VT-100M-D` | 電感 / 功率電感 | SMT | TDK SPM系列 10uH shielded wirewound inductor | [來源](<https://product.tdk.com/en/search/inductor/inductor/smd/info?part_no=SPM6545VT-100M-D>) |
| 47 | `SPM3020T-1R0M-LR` | 電感 / 功率電感 | SMT | TDK SPM-LR 1uH fixed inductor SMD | [來源](<https://www.digikey.com/en/products/detail/tdk/SPM3020T-1R0M-LR/5962317>) |
| 48 | `SPM6530T-4R7M` | 電感 / 功率電感 | SMT | TDK SPM系列 4.7uH power inductor，reflow | [來源](<https://product.tdk.com/en/search/inductor/inductor/smd/info?part_no=SPM6530T-4R7M>) |
| 49 | `XAL1010-103MED` | 電感 / 功率電感 | SMT | Coilcraft XAL1010 high-current shielded power inductor；103=10uH | [來源](<https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xal/xal1010/>) |
| 50 | `SISS5623DN-T1-GE3` | 電晶體 / P-Channel MOSFET | SMT | Vishay P-channel 60V MOSFET，PowerPAK 1212-8S | [來源](<https://www.digikey.tw/zh/products/detail/vishay-siliconix/SISS5623DN-T1-GE3/18723102>) |
| 51 | `NX3008PBKW,115` | 電晶體 / P-Channel MOSFET | SMT | Nexperia 30V P-channel trench MOSFET，SOT323/SC-70 | [來源](<https://bdtic.com/nxp/NX3008PBKW>) |
| 52 | `NX3008PBKW,115` | 電晶體 / P-Channel MOSFET | SMT | Nexperia 30V P-channel trench MOSFET，SOT323/SC-70 | [來源](<https://bdtic.com/nxp/NX3008PBKW>) |
| 53 | `NX7002BKWX` | 電晶體 / N-Channel MOSFET | SMT | Nexperia/NX7002 60V N-channel MOSFET，SOT-23；料號尾碼請核對 | [來源](<https://octopart.com/zh/datasheet/nexperia/NX7002BKWX>) |
| 54 | `BSS84AKW,115` | 電晶體 / P-Channel MOSFET | SMT | Nexperia BSS84AKW 50V P-channel trench MOSFET，SOT323 | [來源](<https://assets.nexperia.com/documents/data-sheet/BSS84AKW.pdf>) |
| 55 | `BSZ040N06LS5ATMA1` | 電晶體 / N-Channel Power MOSFET | SMT | Infineon OptiMOS 60V N-channel power MOSFET，PG-TSDSON-8 | [來源](<https://www.digikey.hk/zh/products/detail/infineon-technologies/BSZ040N06LS5ATMA1/6599580>) |
| 56 | `AOD409` | 電晶體 / P-Channel Power MOSFET | SMT | Alpha & Omega P-channel 60V MOSFET，TO-252/DPAK SMD | [來源](<https://www.digikey.ca/en/products/detail/alpha-omega-semiconductor-inc/AOD409/1855875>) |
| 57 | `RK73H1ETTP1002F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 58 | `RK73H1ETTP2201F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 59 | `RK73Z1ETTP` | 電阻 / 0Ω跳線電阻 | SMT | KOA RK73Z zero-ohm jumper chip resistor | [來源](<https://www.koaspeer.com/products/resistors/heat-shock-resistance/rk73z-at/>) |
| 60 | `RK73H1ETTP1002F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 61 | `RK73H1ETTP3301F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 62 | `RK73H1ETTP1001F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 63 | `RK73H1ETTP3302F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 64 | `RK73H1ETTP4701F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 65 | `RK73Z2BTTD` | 電阻 / 0Ω跳線電阻 | SMT | KOA RK73Z zero-ohm jumper chip resistor；2B尺寸 | [來源](<https://www.digikey.in/en/products/detail/koa-speer-electronics-inc/RK73Z2ATTD/10235990>) |
| 66 | `RK73H1ETTP1003F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 67 | `RK73H1ETTP6801F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 68 | `RK73H1ETTP8201F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 69 | `RK73H1ETTP1502F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 70 | `RK73H1ETTP1003F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 71 | `RK73H2ATTD10R0F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H 10Ω 0805 thick film chip resistor | [來源](<https://www.mouser.com/ProductDetail/KOA-Speer/RK73H2ATTD10R0F>) |
| 72 | `RK73H1ETTP5603F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 73 | `RK73H1ETTP2703F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 74 | `RK73H1ETTP1503F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 75 | `RK73H1ETTP2202F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 76 | `RK73H1ETTP4702F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 77 | `RK73Z1ETTP` | 電阻 / 0Ω跳線電阻 | SMT | KOA RK73Z zero-ohm jumper chip resistor | [來源](<https://www.koaspeer.com/products/resistors/heat-shock-resistance/rk73z-at/>) |
| 78 | `RK73H1ETTP2201F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 79 | `PRL1632-R010-F-T5` | 電阻 / 電流感測低阻值電阻 | SMT | Susumu PRL series current sense resistor，SMD/SMT | [來源](<https://www.mouser.com/ProductDetail/Susumu/PRL1632-R010-F-T5>) |
| 80 | `RK73H1ETTP1501F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 81 | `RK73H1ETTP10R0F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 82 | `RK73H1ETTP4703F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 83 | `RK73H1ETTP3303F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 84 | `RK73H1ETTP6802F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 85 | `RK73H1ETTP3300F` | 電阻 / 厚膜晶片電阻 | SMT | KOA RK73H precision thick film chip resistor | [來源](<https://www.koaspeer.com/products/resistors/general-purpose/rk73h/>) |
| 86 | `RK73Z2ATTD` | 電阻 / 0Ω跳線電阻 | SMT | KOA RK73Z zero-ohm jumper chip resistor，0805 SMD | [來源](<https://www.digikey.in/en/products/detail/koa-speer-electronics-inc/RK73Z2ATTD/10235990>) |
| 87 | `EDZVT2R12B` | 二極體 / Zener 穩壓二極體 | SMT | ROHM 12V Zener diode，EMD2/SOD-523 SMD | [來源](<https://www.digikey.co.nz/en/products/detail/rohm-semiconductor/EDZVT2R12B/4004353>) |
| 88 | `SMDJ30A` | 二極體 / TVS瞬態抑制二極體 | SMT | Littelfuse SMDJ30A TVS diode，surface mount | [來源](<https://www.littelfuse.cn/products/overvoltage-protection/tvs-diodes/surface-mount/smdj/smdj30a>) |

---
整理檔案：`I欄電子元件分類整理.xlsx` → `I欄電子元件分類整理.md`