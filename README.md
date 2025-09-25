# 資料庫系統概論_Final Project
### 實作內容：菇菇栽培圖鑑
<img width="1113" height="541" alt="菇菇栽培圖鑑UI" src="https://github.com/user-attachments/assets/5c32cbd1-aa65-4f2a-b279-aec059c8a30b" />
### Demo影片：https://youtu.be/v0uwyU3PEao

### Database的Schema
* mushroom_dictionary(theme_id, theme_name, id, name, rare_state, rarity, NP)
  1. theme_id：栽培主題對應的編號。
  2. theme_name：每一種菇菇所屬的栽培主題之名稱。
  3. id：每一種菇菇在其栽培主題中的編號。
  4. name：每一種菇菇的名稱。
  5. rare_state：
     * 相同名稱的菇菇可能有2種以上的狀態：普通、稀有。(不是全部的菇菇都有稀有狀態)
     * 普通狀態的菇菇為-1
     * 稀有狀態的菇菇為1、2、……，取決於稀有狀態種類的數量，以此類推。
  6. rarity：每一種菇菇會有相對應的稀有度(1~5星)。
  7. NP：每一種菇菇的賣價。
  8. primary key(name, rare_state)

