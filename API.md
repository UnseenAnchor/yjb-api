# 养基宝 API 文档

本文档整理自：

- 现有 Python 工具 `yjb_tool.py`
- 浏览器插件 `yjb_fund-2.0.0.xpi`
- App 抓包 `Raw_08-28-2026-20-48-20.folder`
- App 包 `养基宝.app` 中可提取的字符串

## 1. 两套 API

| 名称 | Base URL | 来源 | 状态 |
|---|---|---|---|
| 老接口 | `http://browser-plug-api.yangjibao.com` | 浏览器插件 | ✅ 稳定可用 |
| 新接口 | `https://app-api.yangjibao.com` | iOS App | 🟡 部分可用，部分需要 App secret |

命令行通过 `--api old|new` 切换，默认 `old`。

## 2. 认证方式

Token 统一保存在 `~/.yjb_token.json`：

```json
{
  "token": "your-token",
  "timestamp": 1700000000
}
```

请求头差异：

| 接口 | Authorization 示例 |
|---|---|
| 老接口 | `Authorization: <token>` |
| 新接口 | `Authorization: ios:<token>` |

## 3. 签名算法

### 老接口

```text
sign_str = API路径 + token + 时间戳 + SECRET
Request-Sign = md5(sign_str)
```

老接口 secret：

```text
YxmKSrQR4uoJ5lOoWIhcbd7SlUEh9OOc
```

### 新接口（App API）

从 `com.xiaoduotou.yjb_2.0.6_und3fined.ipa`（已解密）逆向得到：

```text
sign_str = https://app-api.yangjibao.com + API路径 + token + SECRET + 时间戳
Request-Sign = md5(sign_str)
```

新接口 secret：

```text
Zk0w9mX7IKFGo5qp5jyDwJKnU7ZJZZJwGhs5myg4vlv4lKEHFKxGe6jlb84KOLkx
```

示例：

```text
GET /account_collect
token = a29c...
timestamp = 1787921148
secret = Zk0w9mX7IKFGo5qp5jyDwJKnU7ZJZZJwGhs5myg4vlv4lKEHFKxGe6jlb84KOLkx

sign_str = https://app-api.yangjibao.com/account_collecta29c...Zk0w9mX7IKFGo5qp5jyDwJKnU7ZJZZJwGhs5myg4vlv4lKEHFKxGe6jlb84KOLkx1787921148
Request-Sign = md5(sign_str)
```

注意：

- 签名时只取路径部分，不带 query。
- 新接口签名包含完整 URL（scheme + host + path）。
- 新接口 secret 已从 2.0.6 解包 IPA 中提取，严格验签接口现已可调用。

## 4. 老接口端点（browser-plug-api）

| 方法 | 路径 | 说明 | CLI |
|---|---|---|---|
| GET | `/qr_code` | 获取登录二维码 | `--login` |
| GET | `/qr_code_state/{id}` | 轮询扫码状态 | `--login` 内部 |
| GET | `/user_account` | 账户列表 | `--accounts` |
| GET | `/account_collect` | 收益汇总 | 仪表盘 |
| GET | `/income_data?account_id={id}` | 单账户收益 | `--income-data ID` |
| GET | `/income_data?collect=true` | 汇总收益 | `--income-data` |
| GET | `/income_line_data?...` | 收益曲线 | `--income-chart` |
| GET | `/fund_hold?account_id={id}` | 基金持仓 | `--holdings ID` |
| POST | `/fund_hold` | 导入/新增持仓 | `--add-holdings` |
| DELETE | `/remove_fund_hold?...` | 删除持仓 | `--remove-holdings` |
| GET | `/index_data` | 指数行情 | 仪表盘 |
| GET | `/notice` | 系统公告 | `--notice` |
| GET | `/version_info` | 版本信息 | `--version-info` |
| GET | `/search_fund?keyword=` | 搜索基金 | `--search` |

## 5. 新接口端点（app-api）

### 5.1 登录/用户

| 方法 | 路径 | 说明 | 当前状态 |
|---|---|---|---|
| POST | `/send_code` | 发送验证码 | ✅ 可用 |
| POST | `/login` | 手机号+验证码登录 | ✅ 可用 |
| GET | `/users/v1/account` | 当前用户信息 | ✅ 可用 |
| GET | `/users/v1/user-account` | 基金账户列表 | ✅ 可用 |
| GET | `/users/v1/fund-group` | 基金分组 | ✅ 可用 |

### 5.2 行情/排行

| 方法 | 路径 | 说明 | 当前状态 |
|---|---|---|---|
| GET | `/market/v1/quote/index-data` | 指数行情 | ✅ 可用 |
| GET | `/market/v1/market-ranking/list` | 市场排行 | ✅ 可用 |
| GET | `/market/v1/market-ranking/hot-funds-ranking` | 热门基金榜 | ✅ 可用 |
| GET | `/market/v1/market-ranking/etf-ranking` | ETF 排行 | ✅ 可用 |
| GET | `/market/v1/market-ranking/theme-ranking` | 板块排行 | ✅ 可用 |
| GET | `/fund_source_list` | 基金来源列表 | ✅ 可用 |
| GET | `/fund_up_down_distribution` | 涨跌分布 | ✅ 可用 |
| GET | `/market_buy_ranking` | 买入排行 | ✅ 可用 |

### 5.3 基金

| 方法 | 路径 | 说明 | 当前状态 |
|---|---|---|---|
| POST | `/content/v1/search/fund` | 搜索基金 | ✅ 可用 |
| GET | `/market/v1/fund/overview` | 基金概览 | ✅ 可用 |
| GET | `/users/v1/fund/detail` | 基金用户详情 | ✅ 可用 |
| POST | `/market/v1/fund/batch` | 批量基金信息 | ✅ 可用 |
| GET | `/position/v1/static/fund-accounts/{id}/funds` | 基金持仓 | ✅ 可用 |
| GET | `/position/v1/option/all` | 全部基金列表（含近一年收益/排名/行业/规模） | ✅ 可用 |
| GET | `/action_record?account_id=&fund_id=&state=&type=&page=&per_page=` | **交易/加仓记录** | ✅ 可用 |
| GET | `/position/v1/chat/get-ini?fund_id=` | AI 对话初始化 | ✅ 可用（返回空数组） |
| GET | `/users/v1/thread/config/option-talent-get` | 持仓页配置开关 | ✅ 可用 |

**`/action_record` 实测说明**（App token 直接可用，无需 wxuk；字段从真实响应提取）：

```json
{ "id": 112577303, "fund_id": "24058", "account_id": 29074061, "type": 2,
  "money": "1655.28", "operation_time": "2026-08-25 14:59:59",
  "state": 2, "confirm_day": "2026-08-26", "fund_name": "华夏港股通央企红利ETF联接A" }
```

- `type`：1=加仓 2=减仓 3=加仓(份额) 4=减仓(份额)；基金转换时 `fund_id` 为 "旧ID,新ID"
- `state`：1=待确认 2=已确认 3/4=已撤销
- `money`：字符串，金额或份额（视 type 而定）
- 遍历全部记录需按基金逐个翻页（`per_page` 最大约 100），参考 `refresh_yjb.py`
| POST | `/market/v1/fund/relation-and-rank` | 关联/排名 | ✅ 可用 |
| GET | `/position/v1/static/fund/hold-stock` | 重仓股 | ✅ 可用 |
| GET | `/market/v1/fund/fund-stock-industry` | 基金行业持仓 | ✅ 可用 |
| GET | `/market/v1/fund-nav/fund-history-nav` | 历史净值 | ✅ 可用 |
| GET | `/market/v1/fund/increase-rate` | 实时涨幅 | ✅ 可用 |
| GET | `/market/v1/fund/gz-data` | 基金估值 | ✅ 可用 |
| GET | `/position/v1/user/funds/all-hold/simple` | 全部持仓简易列表 | ✅ 可用 |
| GET | `/position/v1/user/funds/all-optional/simple` | 全部自选简易列表 | ✅ 可用 |
| GET | `/account_collect` | 收益汇总 | ✅ 可用 |
| GET | `/income_line_data` | 收益曲线 | ✅ 可用 |
| GET | `/inner_notice` | 公告 | ✅ 可用 |

### 5.4 股票

| 方法 | 路径 | 说明 | 当前状态 |
|---|---|---|---|
| GET | `/position/v1/penetrate/hold/stock-overview` | 股票穿透汇总 | ✅ 可用 |
| GET | `/position/v1/penetrate/hold/accounts/{id}/stocks` | 股票穿透明细 | ✅ 可用 |
| GET | `/position/v1/profit-analysis/position-sector` | 持仓行业分析 | ✅ 可用 |
| GET | `/stock_account` | 股票账户 | ✅ 可用 |
| GET | `/stock_account_collect` | 股票收益汇总 | ✅ 可用 |
| GET | `/stock_hold` | 股票持仓 | ✅ 可用 |
| GET | `/stock_income_line_data` | 股票收益曲线 | ✅ 可用 |
| GET | `/stock_optional` | 股票自选 | ✅ 可用 |

### 5.5 自选/达人（部分可用）

| 方法 | 路径 | 说明 | 当前状态 |
|---|---|---|---|
| GET | `/users/v1/optional/talent/group/group-list` | 达人分组 | ✅ 可用 |
| GET | `/users/v1/optional/talent/list-relation` | 达人列表 | ✅ 可用 |
| GET | `/users/v1/optional/subject/group/group-list` | 题材分组 | ✅ 可用 |
| GET | `/users/v1/optional/subject/list` | 题材列表 | ✅ 可用 |
| GET | `/users/v1/optional/subject/header/dates` | 题材日期 | ✅ 可用 |
| POST | `/users/v1/optional/talent/operation/batch-add-talent-to-group` | 批量添加达人 | ✅ 可用 |

### 5.6 从 App 中额外发现、尚未全部接入的接口

App 包里还能提取到大量接口，例如：

- 搜索：`/content/v1/search/composite`、`/content/v1/search/talent`、`/content/v1/search/sector`
- 基金：`/market/v1/fund/batch/paginated`、`/market/v1/us-fund/fund-list`、`/market/v1/us-fund/index-list`
- 持仓管理：`/fund_hold_detail`、`/remove_account_all_fund`、`/fund_hold_sort_top`
- 自选管理：`/users/v1/optional/talent/group/create`、`/users/v1/optional/talent/group/delete`、`/users/v1/optional/talent/operation/move-to-group`
- 用户/客服：`/users/v1/customer-service-chats/identity`、`/users/v1/message/read`
- 股票：`/stock/v1/index-search/search`、`/stock/v1/relation-index/query-batch`、`/stock/v1/relation-index/default-list`

### 5.7 H5 通道（wxapi，逆向自 wx.yangjibao.com H5 包 v2.0.3）

> 与 App 的 `app-api` 不同，这是微信 H5（公众号/小程序/App 内嵌页）使用的独立通道，
> 会话 token（`wxuk`）由微信 OAuth 换发或由 App 打开 H5 时通过 `?wxuk=` 传入，**与 App token 不通用**。

**Base URL**：`https://wx.yangjibao.com/wxapi`

**签名算法**（与 App 新接口同构，secret 不同）：

```
Request-Sign = md5(base_url + path + wxuk + secret + timestamp)
secret = "FI1IUyhfbwOXiAkv1ZUR5WwmlIEsztLn"   # 从 H5 app.js 提取
base_url = "https://wx.yangjibao.com/wxapi"    # 签名用完整域名+路径，不带 query
```

**请求头**：

| 头 | 值 | 说明 |
|---|---|---|
| `Authorization` | wxuk | 免登录接口留空即可 |
| `Request-Time` | unix 秒 | |
| `Version` | `yjb_wxfwh-2.0.3` | |
| `Request-Sign` | 见上 | |
| `User-Agent` | 必须移动端 UA | 否则 `401 非法请求源` |

**实测结论**：
- `401 非法请求源` = UA 不是移动端；`1401 身份信息失效 Err:01` = wxuk 无效/过期（App token、游客 `tourists_visit` 均会被拒）
- 响应包络同 App：`{code:200, message, data}`

| 方法 | 路径 | 说明 | 状态 |
|---|---|---|---|
| GET | `/day_info` | 交易日历 | ✅ 免登录已验证 |
| GET | `/action_record?...` | **交易/加仓记录** | ✅ 同名接口在 app-api 上用 App token 已验证可用；wxapi 版需 wxuk |
| GET | `/fund_profit?fund_id=` | 单基金收益明细 | ⚠️ 需 wxuk |
| GET | `/guiding_record` | 功能引导记录 | 需 wxuk |
| POST | `/user_statistics` | 用户行为统计 | 需 wxuk |
| GET | `/oauth?from_url=` | 微信 OAuth 跳转（wxuk 来源） | 浏览器内流程 |

wxuk 获取方式：① App 内打开 H5 页面（如买卖列表 `wx.yangjibao.com/app/setting/buySellList`）时分享/复制 URL 中的 `wxuk=` 参数；② 手机抓包看 `Authorization` 头。

## 6. CLI 对应关系

| CLI | 接口 | 说明 |
|---|---|---|
| `--sms-login PHONE` | `POST /send_code` + `POST /login` | 新接口登录 |
| `--api new --new-user` | `GET /users/v1/account` | 用户信息 |
| `--api new --new-accounts` | `GET /users/v1/user-account` | 账户列表 |
| `--api new --new-index` | `GET /market/v1/quote/index-data` | 指数行情 |
| `--api new --new-search KEYWORD` | `POST /content/v1/search/fund` | 搜索基金 |
| `--api new --new-holdings [ID]` | `GET /position/v1/static/fund-accounts/{id}/funds` + `POST /market/v1/fund/batch` | 基金持仓 |
| `--api new --new-fund-detail ID` | 多个基金详情接口 | 基金详情 |
| `--api new --new-stock-penetrate [ID]` | 股票穿透接口 | 股票穿透 |
| `--api new --new-market-ranking` | `GET /market/v1/market-ranking/list` | 市场排行 |
| `--api new --new-etf-ranking` | `GET /market/v1/market-ranking/etf-ranking` | ETF 排行 |
| `--api new --new-theme-ranking` | `GET /market/v1/market-ranking/theme-ranking` | 板块排行 |
| `--api new --new-account-collect` | `GET /account_collect` | 基金收益汇总 |
| `--api new --new-income-chart [ID]` | `GET /income_line_data` | 基金收益曲线 |
| `--api new --new-notice [PID]` | `GET /inner_notice` | 公告 |
| `--api new --new-stock-accounts` | `GET /stock_account` | 股票账户 |
| `--api new --new-stock-collect` | `GET /stock_account_collect` | 股票收益汇总 |
| `--api new --new-stock-holdings [ID]` | `GET /stock_hold` | 股票持仓 |
| `--api new --new-stock-income [ID]` | `GET /stock_income_line_data` | 股票收益曲线 |
| `--api new --new-stock-optional` | `GET /stock_optional` | 股票自选 |
| `--api new --new-fund-distribution` | `GET /fund_up_down_distribution` | 基金涨跌分布 |
| `--api new --new-option-all` | `GET /position/v1/option/all` | 全部基金列表 |
| `--api new --new-hot-funds` | `GET /market/v1/market-ranking/hot-funds-ranking` | 热门基金榜 |
| `--wx-day-info` | wxapi `GET /day_info` | H5 交易日历（免登录） |
| `--wxuk TOKEN --wx-action-record ACCOUNT_ID` | wxapi `GET /action_record` | H5 交易/加仓记录 |
| `--wxuk TOKEN --wx-fund-profit FUND_ID` | wxapi `GET /fund_profit` | H5 单基金收益 |

## 7. 加仓记录导出工具

`refresh_yjb.py`：一键拉取全部账户、全部基金的加仓/减仓记录并导出 Excel + JSON。

```bash
python refresh_yjb.py send  <手机号>   # 发送验证码
python refresh_yjb.py pull  <验证码>   # 登录 + 拉取 + 导出 加仓记录_导出.xlsx
python refresh_yjb.py export           # 用现有 token 直接导出（未过期时）
```

注意：`加仓记录_raw.json` / `加仓记录_导出.xlsx` 是个人财务数据，已被 .gitignore 排除，勿提交。
