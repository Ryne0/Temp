# EMS 極性注意表

更新日期：2026-09-20

> 用途：打件前快速確認有極性／有方向性的零件。  
> 注意：本表是工作預審用，最終仍以 MPN Datasheet、客戶 Assembly/Polarity drawing、PCB/Gerber/實板標示為準。

## 需要優先確認極性的零件

| BOM序號 | MPN | 類型 | 是否有極性 | 元件本體辨認重點 | 極性圖建議標示 |
|---:|---|---|---|---|---|
| 6 | GYB1V151MCQ1GS | 鋁電解電容 | 有 + / - | 外殼負極側有 Negative polarity 標示 | 直接標 + / - |
| 12 | UUD1H151MNL1GS | 鋁電解電容 | 有 + / - | 依 Datasheet Positive / Negative 判定 | 直接標 + / - |
| 13 | ADCR-X02R7SB105PT | Supercapacitor | 有 + / - | 負極側套管有 negative bar | 直接標 + / - |
| 24 | V8P10-M3/86A | Schottky diode | 有 A / K 方向 | 有 1 個 Cathode K、2 個 Anode pad | 標 K / A，不要標成普通兩腳二極體 |
| 25 | SMF12A-E3-18 | TVS | 有 A / K 方向 | Band 側為 Cathode | 標 K / A |
| 26 | RB068MM-60TFTR | Schottky diode | 有 A / K 方向 | Marking bar 側為 Cathode | 標 K / A |
| 72 | EDZVT2R12B | Zener diode | 有 A / K 方向 | Cathode band 側為 K | 標 K / A |
| 73 | SMDJ30A | TVS | 有 A / K 方向 | Color band 側為 Cathode | 標 K / A |

## 方向性零件（不一定有正負極，但不可任意旋轉）

### IC
- LMR51450FSQDRRRQ1
- LMR51420YDDCR
- MAX38888ATD+T
- MAX40203AUK+T
- LM25117PMHX/NOPB
- TLV7022DDFR
- TLV9062IDDFR

確認方式：**Pin 1、缺口、圓點、斜角、Footprint Pin 1**。

### MOSFET / Transistor
- NX3008PBKW
- NX7002BKWX
- BSS84AKW
- BSZ040N06LS5
- AOD409

確認方式：**G / D / S 腳位 + Footprint Pin numbering**，不要用正負極概念判斷。

### Connector
確認方式：**Pin 1 / Key / 插接方向**。

## 客戶符號暫定規則

目前已知案例：

- 該客戶圖面上的 **ㄇ字型標示側 = Zener/TVS 的 Cathode（K）**
- 這個規則可作為同客戶其他板子的高優先級線索，但新板建議至少抽查 1 顆可驗證元件後再全板沿用。
- **不要把 K 直接理解成負電位。** K 是 Cathode 端名稱；在線圈箝位、TVS、Zener 等電路中，K 很常接較高電位。

## 快速判讀規則

- 鋁電解：外殼色帶通常標 **負極 -**
- 鉭電容：很多系列的色帶／標記反而標 **正極 +**，務必查 Datasheet
- Diode / Zener / TVS：Band / Bar 常用來標 **Cathode K**
- 雙向 TVS：通常沒有安裝方向問題，但仍須確認 MPN 確實為 Bidirectional
- IC：看 **Pin 1**
- MOSFET：看 **G / D / S**
- Connector：看 **Pin 1 / Key**

## Gerber 判讀時的順序

1. 先從 BOM 確認 MPN 與元件類型。
2. Datasheet 確認 + / -、A / K 或 Pin 1。
3. 找 PCB 對應 Pad。
4. 先找 GND / +V / Connector / 大電解等容易辨認的 Net。
5. 再沿走線確認 Coil、MOSFET、IC 等。
6. 最後才用電路功能做 sanity check。

### 常見箝位概念

線圈 + Zener / TVS 常見情況：

```text
+V ---- K [Zener/TVS] A ---- Switching Node
```

所以 **Cathode（K）並不代表一定接負電位**。
