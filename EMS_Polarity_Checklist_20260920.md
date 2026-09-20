# EMS 極性注意表

更新日期：2026-09-20（v2）

> 用途：打件前快速確認哪些零件「真的需要列入產線極性圖」、哪些只是有方向、哪些其實無極性。  
> 注意：本表是工作預審用，最終仍以 MPN Datasheet、客戶 Assembly/Polarity drawing、PCB/Gerber/實板標示為準。

## 產線判斷先分三類

| 分類 | 代表零件 | 是否列入產線極性圖 | 現場重點 |
|---|---|---|---|
| 真正有極性 | 鋁電解、Zener、Diode、單向 TVS | **要** | 標 + / - 或 A / K |
| 有固定方向但不是正負極 | IC、MOSFET、部分 Connector | **視公司格式而定，通常標 Pin 1 / Key** | 不可任意旋轉 |
| Datasheet 明確 No polarity | 一般 R、MLCC、部分 Inductor / Common Mode Choke | **不要當極性件標** | 客戶 Gerber 即使有 Pin 1 / 方位記號，也不代表有極性 |

---

## 需要優先確認極性的零件

| BOM序號 | MPN | 類型 | 極性/方向 | 是否列入產線極性圖 | 元件本體辨認重點 | 極性圖建議標示 |
|---:|---|---|---|---|---|---|
| 6 | GYB1V151MCQ1GS | 鋁電解電容 | 有 + / - | **要** | 外殼負極側有 Negative polarity 標示 | 直接標 + / - |
| 12 | UUD1H151MNL1GS | 鋁電解電容 | 有 + / - | **要** | 依 Datasheet Positive / Negative 判定 | 直接標 + / - |
| 13 | ADCR-X02R7SB105PT | Supercapacitor | 有 + / - | **要** | 負極側套管有 negative bar | 直接標 + / - |
| 24 | V8P10-M3/86A | Schottky diode | 有 A / K 方向 | **要** | 有 1 個 Cathode K、2 個 Anode pad | 標 K / A，不要標成普通兩腳二極體 |
| 25 | SMF12A-E3-18 | TVS | 有 A / K 方向 | **要** | Band 側為 Cathode | 標 K / A |
| 26 | RB068MM-60TFTR | Schottky diode | 有 A / K 方向 | **要** | Marking bar 側為 Cathode | 標 K / A |
| 72 | EDZVT2R12B | Zener diode | 有 A / K 方向 | **要** | Cathode band 側為 K | 標 K / A |
| 73 | SMDJ30A | TVS | 有 A / K 方向 | **要** | Color band 側為 Cathode | 標 K / A |

---

## 特別案例：Gerber 有標記，但元件其實無極性

| MPN | 類型 | Datasheet 判定 | 是否列入產線極性圖 | 備註 |
|---|---|---|---|---|
| ACM1211-102-2PL-TL01 | Common Mode Choke | **No polarity** | **不要當極性件標** | 四腳、兩組繞組；客戶 Gerber 即使有單腳/Pin 1 方位標記，也不代表需要極性方向 |

### ACM1211-102-2PL-TL01 判讀重點

它的概念是兩條線各自穿過一組線圈：

```text
Line 1 IN  ----[ winding 1 ]---- Line 1 OUT
Line 2 IN  ----[ winding 2 ]---- Line 2 OUT
```

- 不是「兩正兩負」。
- 不是 Zener/Diode 那種 A/K 極性。
- Datasheet 為 No polarity 時，不因 Gerber 有 Pin 1 標示就把它列成極性件。
- 若只是 CAD library 的 orientation mark，可保留在 Assembly/位置識別用途，但不要誤解成「裝反會造成極性錯誤」。

---

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

這類不要標 + / -；若產線需要方向圖，改標 **Pin 1**。

### MOSFET / Transistor

- NX3008PBKW
- NX7002BKWX
- BSS84AKW
- BSZ040N06LS5
- AOD409

確認方式：**G / D / S 腳位 + Footprint Pin numbering**，不要用正負極概念判斷。

### Connector

確認方式：**Pin 1 / Key / 插接方向**。

---

## 客戶符號暫定規則

目前已知案例：

- 該客戶圖面上的 **ㄇ字型標示側 = Zener/TVS 的 Cathode（K）**。
- 這個規則可作為同客戶其他板子的高優先級線索，但新板建議至少抽查 1 顆可驗證元件後再全板沿用。
- **不要把 K 直接理解成負電位。** K 是 Cathode 端名稱；在線圈箝位、TVS、Zener 等電路中，K 很常接較高電位。
- **也不要反過來認為客戶所有特殊符號都代表極性。** 先查 MPN Datasheet 是否真的有 polarity / orientation requirement。

---

## 快速判讀規則

- 鋁電解：外殼色帶通常標 **負極 -**
- 鉭電容：很多系列的色帶／標記反而標 **正極 +**，務必查 Datasheet
- Diode / Zener / TVS：Band / Bar 常用來標 **Cathode K**
- 雙向 TVS：通常沒有安裝方向問題，但仍須確認 MPN 確實為 Bidirectional
- IC：看 **Pin 1**
- MOSFET：看 **G / D / S**
- Connector：看 **Pin 1 / Key**
- Common Mode Choke：先查 Datasheet 是否 **No polarity**，不要看到 Gerber 有方位符號就直接列成極性件

---

## Gerber 有特殊符號時，先做這個判斷

```text
Gerber 有特殊標記
        ↓
先查 MPN / Datasheet
        ↓
是否明確有 Polarity？
   ├─ 是 → 列入極性圖，標 + / - 或 A / K
   └─ 否
       ↓
是否只是 Pin 1 / Orientation / Key？
   ├─ 是 → 視產線需要標 Pin 1 / Key
   └─ Datasheet = No polarity → 不列為極性件
```

---

## Gerber 判讀時的順序

1. 先從 BOM 確認 MPN 與元件類型。
2. Datasheet 確認 + / -、A / K、Pin 1，或是否明確標示 No polarity。
3. 再看客戶 Gerber 的特殊符號代表什麼。
4. 找 PCB 對應 Pad。
5. 先找 GND / +V / Connector / 大電解等容易辨認的 Net。
6. 再沿走線確認 Coil、MOSFET、IC 等。
7. 最後才用電路功能做 sanity check。

### 常見箝位概念

線圈 + Zener / TVS 常見情況：

```text
+V ---- K [Zener/TVS] A ---- Switching Node
```

所以 **Cathode（K）並不代表一定接負電位**。

更準確的記法是：

> Zener 在使用齊納崩潰特性時，K 的電位要高於 A；是否接「正電源」仍要看實際電路用途。
