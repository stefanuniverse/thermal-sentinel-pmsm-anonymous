# Final public-release audit / 最终公开前审核

审核日期：2026-11-07（Asia/Shanghai）

项目：Thermal Sentinel PMSM v0.1.0

对外署名：**StefanUniverse**（开发者笔名）

目标：`stefanuniverse/thermal-sentinel-pmsm-anonymous`

被审核的科学代码提交：`c65f7314be28cb3c44f36c5bd5a0a6680f350b3a`

**结论：关键项目 PASS；未发现 BLOCKER。仍保持 Private，等待所有者单独明确回复“确认公开”。本报告不是公开授权，也不是已公开的发布报告。**

本次检查重新运行，不以历史“通过”代替本次证据。阶段一未改变任何已跟踪文件；阶段二只增加本报告。没有修改实验结果、数据、模型、UI、其他项目或其他仓库，没有改写历史或强制推送。

## 1. 仓库身份与可见性 — PASS

| 检查 | 本次实际结果 |
|---|---|
| 唯一 remote | `origin`；fetch/push 均为 `https://github.com/stefanuniverse/thermal-sentinel-pmsm-anonymous.git` |
| 远程身份 | GitHub API 返回所有者/名称与上述目标完全相同 |
| 登录账号 | `stefanuniverse`，与预期账号一致 |
| 当前/默认分支 | `codex/anonymous-release` |
| 审核开始时本地及远程 HEAD | 均为上述 `c65f731…` |
| 可见性 | **Private**；未执行 visibility 修改 |
| 分支、Tag | 远程一个分支、零 Tag；本地分支及 origin 跟踪 ref 指向同一历史 |
| 额外 remote | 无 |
| 历史 | 两次可达提交、64 个不同历史 blob；干净根提交无父提交 |

所有者已明确纠正本次目标为带 `-anonymous` 后缀的仓库。不能将旧备份仓库当成这个目标，也不能将其旧提交导入本仓库。

本报告如通过普通提交保存，会新增一个仅含报告的笔名提交；科学代码被审核对象仍明确固定为 `c65f731…`。最终公开前仍须再次核对最新 HEAD、完整历史和变更清单。

## 2. 匿名化及凭据检查 — PASS；账号关联风险 WARN

- 对 59 个发布文件、完整暂存树、所有可达提交和历史文件版本重新扫描。
- 所有 Author、Committer 均为笔名，邮箱为所有者从 GitHub Settings > Emails 提供的准确 ID 型 noreply 地址；与 GitHub API 返回的账号 ID/用户名一致。报告不重复打印私人身份值。
- 本地保留的 11 种中文、分隔/紧凑及拼音姓名变体继续参与扫描，没有通过删规则获得 PASS。
- README、两类许可证、自有来源记录、CFF、包元数据、源码、测试、HTML/JavaScript、配置和文件名未发现已知私人身份或个人目录匹配。
- 当前及历史文本对象额外检查 GitHub/provider token、JWT、私钥、含凭据 URL、常见云密钥及可疑密码赋值；**零命中**。这不是对所有未知凭据格式的数学保证。
- PDF 的 Info/XMP/文本/附件、PNG 文本与 EXIF/GPS、SVG 文本已检查；未发现私人身份。没有 Office 文件或 Notebook，也没有 Notebook 输出需要发布。
- 新构建 wheel 的 18 个成员检查通过，解析后的包 Author 是笔名，无私人邮箱或路径发现。构建产物本身不上传。
- 自有 CFF/包作者没有学校、单位或 ORCID。文档中的 Paderborn University 等是必要的第三方数据归属，不是所有者单位，不能删除或伪称为团队身份。
- GitHub 账号公开 name、email、bio、company、location、blog 字段本次均为空；没有修改账号资料。头像、其他外部页面和既有社会关联不由此证明匿名。

### GitHub 其他发布面 — PASS

本次 API 核对无 Tag、Release、Issue/PR、评论、讨论、部署、Actions run 或 artifact，wiki 关闭；仓库没有 Actions 配置，因此不存在本仓库的 Actions 公开日志或构建产物需要清理。没有创建 Release、PyPI 发布或新服务。

## 3. Git 历史检查 — PASS

两次提交及全部历史 blob 的身份/凭据检查通过；提交信息和作者字段均受检查。不仅检查最新工作区，也检查已被后续版本替换的文件。没有额外分支或带身份的 Tag。

本次不会重建 Git 历史、删除旧资料或 force push。旧备份保持独立；不得通过 merge/cherry-pick 将其身份历史带回这里。Git 扫描不能清除服务器缓存、第三方既有克隆、其他账号信息或不可达对象的外部副本。

## 4. 数据与知识产权 — PASS；没有许可不明 BLOCKER

| 对象 | 核查结果及边界 |
|---|---|
| 自主代码/文档 | 所有者此前已确认权属与 MIT 选择；版权署名使用其授权的笔名。MIT 范围不覆盖第三方数据 |
| 原始 TNN 类代码 | 重新获取固定上游版本；两段类 AST 与本地一致，原作者 MIT 全文与本地 notice 一致，合法署名保留 |
| Paderborn 数据 | 官方 Kaggle API 本次返回 v3、CC BY-SA 4.0；原始 ZIP/CSV 不在 Git，数据许可未被改写为 MIT |
| 聚合表格和图 | 单独 `reports/LICENSE` 为 CC BY-SA 4.0，保留数据归属、许可证链接及分析改动说明 |
| 论文/预训练权重/CAD/商业工程 | 发布树及全部历史中没有原始论文全文、第三方模型权重、原始 CAD 或商业仿真工程 |
| 可重建原始时序的附件 | 发布参考 JSON 只有聚合/分 profile 指标及训练诊断，无完整 y/prediction/input 时序；原始行及最差样本字段未发布 |
| NOTICE | 无独立顶层 NOTICE；所复制 MIT 代码的完整版权/许可在 `third_party/LICENSE-TNN`，固定来源与改动在 `third_party/PROVENANCE.md`。未发现另需复制的上游 NOTICE |

依据：[固定上游 MIT](https://raw.githubusercontent.com/wkirgsn/thermal-nn/531f2275adcbb9ad562dd59cb1c8043630ae0e11/LICENSE)、[原始数据](https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature)、[CC BY-SA 4.0 条款说明](https://creativecommons.org/licenses/by-sa/4.0/)。本审核是软件与来源核对，不代替特殊机构权属争议的法律判断。

### 上游 notebook 校验值解释 — WARN，非代码/许可冲突

GitHub 固定版本提供的 LF 文件 SHA-256 为：
`82fbcd40ad88ac38932698fcbe42eb8abab56e82703ceb0320513dd878d005f4`。

现有来源文档的 `1ac66752…` 对应相同内容转成 Windows CRLF 后的 SHA-256；本次实际转换后与其完整记录一致。两段类的 AST 也一致。因此不是换用未知代码或许可不明，但引用校验值时必须说明换行形式，不能声称二者为同一字节流。

## 5. 科研内容及数据隔离 — PASS；适用性限制 WARN

README 有中英文科研定位、数据版本/来源、环境、运行方式、真实对照、负面结果和局限；CFF 1.2 官方 schema 本次验证通过。没有把短预算 TNN、单电机单数据集单种子实验宣传为跨电机、工业部署、硬件实时或永磁体保护控制。

代码及实跑核对：

- 完整 69 个 `profile_id` 先分成 train 40 / validation 9 / calibration 12 / test 8，再分别 stride-20 取样。没有跨 profile 连接窗口。
- StandardScaler、输入中位数、故障幅值尺度、输入重建器和 TNN 电量归一化只在训练 profile 拟合。
- validation 只用于 TNN checkpoint 选择；calibration 用于残差区间宽度；测试目标没有进入模型拟合或归一化。
- `pm` 和定子温度不在七个推理输入中。TNN 和 LPTN 的测试初态来自 ambient/coolant，未用实测目标温度初始化。
- EWMA、缺失前向填充及 LPTN 状态更新为因果路径；相应回归测试本次通过。
- 测试组有固定指定 profile，且这些测试 profile 已在探索开发中反复查看；不能把它们称为新预注册、完全未触及的外部盲测集。现有局限已承认这一点。
- 全部五种方法、六种条件和八个测试 profile 的结果保留；代理热特征在掉线/偏置下退化、短训练 TNN 不如 Ridge、热启动及区间失效没有被删除。
- 10 秒步长、合成 i_q 故障、有效 LPTN 比值而非绝对 R/C、经验区间而非通用安全保证均明确标注。

## 6. 本次实际安装、测试及复现

使用审核提交的独立文件快照及**新建** Python 3.12.3 venv；没有系统 site-packages，没有加载旧权重。模块确实从审核快照导入。所有原始数据拷贝、权重、回放、日志和截图留在被 Git 忽略的本地审核目录。

| 本次运行项目 | 状态 | 实际结果 |
|---|---|---|
| README 依赖安装及 editable install | PASS | 两条安装命令均成功，`pip check` 通过；安装阶段约 197.979 秒 |
| 运行版本 | PASS | NumPy 1.26.4、SciPy 1.13.1、sklearn 1.5.2、Torch 2.7.1+cpu、matplotlib 3.9.4；与核心固定版本一致 |
| 可选审核依赖安装 | PASS | `requirements-audit.txt` 安装成功 |
| 全部自动测试 | PASS | **16/16，零跳过**；覆盖 profile 隔离、因果性、故障通道、指标、TNN 输出/参数量、LPTN、HTTP 防护和身份扫描 |
| 真实数据获取 | PASS | README 的本地官方 v3 ZIP `--source` 路径成功，ZIP 与 CSV 两个 SHA-256 均核对 |
| 数据预处理 | PASS | 本次读到 1,330,816 行、69 profile，四组划分相符 |
| 模型训练与评估 | PASS | 两个 TNN 变体各 10 epoch，从头训练；全部五方法/六条件重算，约 65.169 秒 |
| 冻结值复现 | PASS | **4212** 个非计时数值，最大绝对差 **0**；CPU 计时明确排除 |
| CSV/图导出 | PASS | 30 行方法/条件表、240 行 profile 表与已发布 CSV 数值完全一致；图导出成功 |
| LPTN 补充基线 | PASS | 两种结构 × 六条件重新运行，约 11.149 秒；没有修改冻结比较值 |
| wheel 与作者元数据 | PASS | 成功构建；18 个成员身份/路径检查通过 |
| CFF | PASS | 官方 1.2.0 tagged schema，零格式错误，作者为笔名 |
| 现有演示启动 | PASS | 新环境通过 `python -m thermal_sentinel.demo` 启动，loopback HTTP 正常，测试后停止 |
| 浏览器桌面/移动视窗 | PASS | 新生成真实结果；1440×1060 和 390×844 的 Edge 自动化通过，无页面错误或横向溢出 |
| 演示交互 | PASS | profile 46、outage、游标、揭晓、五方法结果、播放/暂停正常；原始 ZIP、权重、环境、Git 路径和目录穿越请求为 404 |
| 第一阶段来源保持 | PASS | 原有全部 59 个跟踪文件在审计期间 SHA-256 不变；未替换报告结果 |

### 运行范围及未实测部分 — WARN

1. **没有 Streamlit 应用或依赖。** 此项不能伪报为 Streamlit 启动通过；本次实际通过的是仓库已有 Python HTTP + HTML/JavaScript 演示。没有为了审核新建第二套 UI。
2. 本次没有重新传输 122 MB Kaggle ZIP；实际验证了官方本地 ZIP 的双 hash 和支持的手动获取路径。可选 `--download` 的登录/网络行为未完全验证，官方当前版本/许可元数据已在线核查。
3. 科学包按 README 安装，核心版本已核对；完整 transitive lock 在所有操作系统上的重新解析、未来漏洞数据库审计、Linux/macOS、实体 iPhone/Safari和硬件部署没有在本轮冒充通过。
4. 浏览器的隐藏/揭晓只是本地演示交互，不是保密边界。loopback 服务不应直接作为互联网生产服务。
5. 单次 CPU 重现实验仍不能替代多随机种子、真实传感器故障、跨电机外部验证或工业保护认证。

## 7. 未解决问题、风险与发布建议

| 项目 | 状态 | 处理意见 |
|---|---|---|
| 已知身份、私密邮箱、密钥发现 | PASS | 本次集合中零发现；报告和日志不输出敏感匹配原文 |
| 来源不明/无授权原始文件 | PASS | 本次集合中未发现此类 BLOCKER；不得在后续提交添加原始数据或新附件而跳过审核 |
| 账号整体匿名性 | WARN | noreply/笔名不等于不可关联；仍需所有者判断头像、外链、既有账号关联及机构义务 |
| 源码字节 hash 的 LF/CRLF 区别 | WARN | 上述差异已实测解释；算法代码与许可未变 |
| 没有独立 NOTICE / 没有 Streamlit | WARN | MIT notice 已完整保留；现有演示可运行。不声称不存在的文件或框架已测试 |
| 实验外推与验证范围 | WARN | 保留现有负面结果和局限，不宣传工业级/跨电机结论 |
| 最终公开确认 | WARN / 发布门禁 | **尚未收到本阶段后的“确认公开”，必须维持 Private** |

**推荐：可进入所有者最终确认阶段；不自动公开。**

收到明确“确认公开”后，须重新核对这个准确仓库、Private 状态、授权账号、最新提交、所有新增文件和完整 refs。仅在复核仍通过时才可执行指定仓库的可见性转换。不得顺带创建 Release、发布 PyPI、部署服务、改动旧备份或其他项目。

本报告不会声称仓库已经 Public；正式公开后的地址、日期、最终提交和访问/克隆验证应另写 `FINAL_PUBLIC_RELEASE_REPORT.md`，不能提前生成成功结论。
