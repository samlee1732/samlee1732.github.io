# SenseDex Lab 首页

SenseDex Lab（Sensing and Dexterous Manipulation，感知与灵巧操作实验室）的静态首页，适合直接部署到 GitHub Pages。没有构建步骤，无须安装 Node.js 或任何依赖。页面不依赖第三方字体、脚本或图片服务。

## 本地查看

直接打开 `index.html`，或者在此目录执行：

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

然后访问 `http://127.0.0.1:8080`。

## 发布到 GitHub Pages

1. 创建或选择一个 GitHub 仓库。使用 GitHub Free 时，选择公开仓库。
2. 将此目录内的全部文件放到仓库根目录，确保 `index.html`、`assets/` 和 `.nojekyll` 均已提交。
3. 打开仓库 **Settings → Pages**。
4. 在 **Build and deployment → Source** 选择 **Deploy from a branch**。
5. 选择文件所在分支（通常为 `main`）和 **/(root)**，点击 **Save**。
6. 等待部署完成，使用 Settings → Pages 显示的网址访问。

个人主页可使用名为 `你的用户名.github.io` 的仓库，网址为 `https://你的用户名.github.io/`。普通项目仓库的网址为 `https://你的用户名.github.io/仓库名/`。资源全部采用相对路径，两种方式均可使用。后续修改并提交到发布分支后，GitHub Pages 会自动更新网站。

官方说明：
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## 修改内容

- `index.html`：实验室名称、简介、导航和弹窗内容。
- `assets/styles.css`：配色、字体、间距、桌面和手机布局。
- `assets/main.js`：手机菜单、Teaching 下拉菜单、信息弹窗和站内搜索。
- `assets/search-index.json`：由生成脚本提取页面内容生成的站内搜索索引。

页面视觉参考用户提供的截图。中英文简介按作者新提供的个人经历更新，英文为对应译文；中文修正了“EEE → IEEE”和“2026毕业 → 2026年毕业”两处笔误，并依据作者个人站点统一了职称与学校名称。履历、论文数量及项目经历由作者提供，未做外部核实。

Under Review 导航位于 Publication 前，跳转到联系方式下方的在审稿件区；Publication 导航跳转到其后的已发表论文展示区，点击已发表论文标题可打开独立详情页；Team 展示作者提供的概览信息，成员名单仍需补充；Teaching 展示《机器人学及应用》和《自动控制原理》两门课程，课程资料仍需补充。右上角放大镜打开站内搜索，联系方式仍保留在首页 `#contact` 区域，可搜索“邮箱”或“联系方式”进入；手机端点击页内导航后会先收起导航菜单。网站采用玫红、紫色到深蓝的渐变，实验室标题、导航选中线、搜索图标与下拉面板顶边保持一致。

顶部导航的 News 位于 Teaching 之后，跳转到页面下方的 `#news` 动态区。目前显示待更新提示；后续在 `index.html` 的该区域替换为真实的日期和动态内容即可。窄屏导航在 1200px 及以下收进菜单，点击 News 会收起菜单并跳转。

## 论文展示与维护

### 在审稿件

`data/under-review.json` 单独维护在审稿件，与下方 8 篇已发表论文分开展示。目前录入作者提供的 Materials & Design 投稿：**A Torsionally Tristable Metastructure with In-Plane Translational Actuation and Post-Fabrication Angle Tuning**，稿号 `JMADE-D-26-07879`。通讯作者为 Tao Luo，共同作者为 Ruyang Yu、Sen Li；按角色展示，不推断正式作者排序。状态仅标为 Under Review，未填写发表年份、DOI、卷期或录用信息。

摘要、BibTeX 和图片/视频保留待补充位置，缺失资源不生成链接。当前不生成该稿件的独立详情页或引用文件。补充图片时可使用与已发表论文相同的 `image`、`image_alt`、`image_width`、`image_height` 字段，将文件放入 `assets/publications/`。新增或修改在审稿件后运行下方生成命令，同步更新首页和站内搜索；后续补齐摘要、引用等资源时再启用对应入口。

### 已发表论文

论文采用“主页概览 + 独立详情页”的结构。主页保留左侧引用信息、右侧图片或动图，手机端上下排列；详情页包含作者、发表信息、DOI、Abstract / Summary、Links 和可下载的 BibTeX。设计参考：https://bionicdl.ancorasir.com/?p=2124 。

已从作者个人网站 http://www.senli.site/ 迁入 6 篇期刊与会议论文，并根据作者指定的 [ORCID 记录](https://orcid.org/0000-0002-4436-9294) 补入 2 篇，共 8 篇，按年份降序排列。现有 7 项配图、4 份 PDF 和 3 个视频链接。没有导入学位论文或非论文项目。图片和 PDF 存放在本仓库，加载时不依赖原站；列表图片使用懒加载并保留原始 GIF 动画。

引用信息已用论文原文、出版社页面及出版社提交的 Crossref 元数据复核；新增两篇的摘要保留原文，并附 CC BY 4.0 来源链接：

- ActiveSPN：2025，10(8)，8115–8122，已发表。
- ActiveSPN2：2026 年在线发表，文章号 100326；尚未确认的卷期留空。提供的 PDF 为作者预印本，链接已标明。
- Teaching oral care：2025，5(3)，文章号 36。
- ADAP：2025，6，204–219。
- Active Surface：2024 ReMAR，627–632；作者顺序依据论文原文。
- Flip-and-Flap：2021，6(3)，5199–5206；补齐原站遗漏的两位共同作者。
- Stable High-Speed Quadrotor Flight：2021，Mathematical Problems in Engineering，文章号 9825790。
- Parameter Adaptive Control：2021，IEEE Access 9，139958–139967；配图保留待补充位置。新增两篇暂无本地 PDF / 视频文件，保留待补充提示和出版社入口。

4 份现有 PDF，以及新增两篇论文的出版社/发表版本原文中的正式摘要已录入 Abstract；Oral care 和 ADAP 暂保留作者个人站的简介，标为 Summary，并保留完整摘要、PDF 和视频的待补充提示。没有用简介冒充正式摘要。BibTeX 只写入已核对的字段；每篇的来源链接记录在 `data/publications.json` 的 `metadata_sources` 中。目前展示的 8 篇与本次核对的 ORCID 公开论文记录一致；后续新增论文仍需单独维护。

维护步骤：

1. 修改 `data/publications.json` 中对应论文；新增论文时复制一个对象，使用唯一的 `id`（小写字母、数字和连字符），填写真实作者顺序、标题、刊物、年份和资源信息。
2. 将图片或 GIF、PDF 放入 `assets/publications/`，在 `image` / `pdf` 中填写文件名。没有配图时省略 `image`，页面自动显示待补充位置。有图片时应同时填写 `image_alt`、`image_width`、`image_height`；视频填真实的 `video` 链接。
3. 正式摘要填入 `abstract`；只有简介时保留 `summary`。补齐资料后，待补充提示会自动消失。引用可使用 `volume`、`number`、`pages`、`article_number`、`doi` 等字段；没有确认的信息不要猜填。
4. 在仓库根目录运行：

   ```sh
   python3 tools/build_publications.py
   ```

   脚本仅依赖 Python 3 标准库，更新首页的 Under Review 和 Publication 区域，并为已发表论文生成 `publications/<id>/index.html` 与 `citation.bib`。简介、联系方式、News 和域名文件均保留。不要直接修改生成的论文条目或详情页，否则下次生成会覆盖修改。

5. 本地预览后，将 JSON、素材、生成的 HTML / BibTeX 一起提交到 `main`。GitHub Pages 直接发布生成好的文件，无需在服务器运行 Python。

样式在 `assets/styles.css`；详情页复用首页导航与弹窗。首页导航改动后重新运行脚本即可同步。删除论文时也应手动清理其旧详情页目录，避免旧链接继续保留。

## 站内搜索

导航右侧原 Contact 按钮已替换为放大镜。点击展开搜索框，输入内容即时匹配，按 Enter 或右侧箭头确认并聚焦首条结果；点击结果打开论文、跳转首页对应区域，或打开 Team / Teaching 面板。按 Esc、点击外部或 Tab 移出搜索区域可收起。手机端放大镜始终可见，不必先打开导航菜单。

搜索覆盖 8 篇已发表论文的标题、作者、年份、DOI、摘要，在审稿件的标题、期刊、作者角色与稿号，以及中英文简介、联系方式、News、Team 和两门课程。在审搜索结果单独标注 Under Review。支持中英文关键词和多个词同时匹配，结果按标题相关度排序。无匹配时显示提示。搜索在浏览器本地完成，不调用外部搜索服务，不保存或上传查询词。

修改简介、联系方式、课程、新闻或论文后运行 `python3 tools/build_publications.py`，并提交生成的 `assets/search-index.json` 和详情页。索引中的搜索文本来自实际页面内容；显示摘要与辅助匹配关键词分开。新内容不会在发布时自动抓取。直接双击 HTML 时，浏览器可能限制索引读取，请通过上面的本地 HTTP 服务预览。

## 本项目的部署位置

- 仓库：https://github.com/samlee1732/samlee1732.github.io
- 自定义域名：https://www.sensedex.online/
- GitHub Pages 默认地址：https://samlee1732.github.io/
- 发布来源：`main` 分支的仓库根目录（`/`）。

推送到 `main` 后，GitHub Pages 自动发布更新。部署进度可在仓库的 Actions 或 Settings → Pages 查看。

## 购买域名后的解析与绑定

本项目已通过根目录的 `CNAME` 文件绑定 `www.sensedex.online`。文件只填写域名，不包含协议或路径：

```text
www.sensedex.online
```

保留该文件即可在后续发布时保持域名配置；它不会代替域名服务商的 DNS 记录。以下记录完整的绑定与解析步骤。

1. **先在 GitHub 绑定域名**：打开本仓库 **Settings → Pages**，在 **Custom domain** 填写 `www.sensedex.online`（不带 `https://`），点击 **Save**。本项目从分支发布，保存后 GitHub 会在仓库根目录生成 `CNAME` 文件；后续更新网站时保留此文件，并先拉取 GitHub 上的新提交。
2. **再添加 DNS 解析**：进入域名服务商的 DNS 管理页面（截图使用 DNSPod），按下表添加记录。

   | 主机记录 | 记录类型 | 线路类型 | 记录值 | TTL（秒） |
   | --- | --- | --- | --- | --- |
   | `www` | `CNAME` | 默认 | `samlee1732.github.io.` | `600` |

   记录值只填写 GitHub Pages 主机名，不加协议、路径或仓库名。末尾的 `.` 表示完整域名；部分控制台会自动补上或省略它。同一个 `www` 主机记录不要同时保留冲突的 A、AAAA 或其他 CNAME 记录。

3. **等待生效并开启 HTTPS**：回到 **Settings → Pages** 查看 DNS 检查结果。DNS 传播和 HTTPS 证书准备都可能需要等待，最长各约 24 小时。待 **Enforce HTTPS** 可用后勾选，再访问 `https://www.sensedex.online/` 确认页面和 HTTPS 正常。

上述 CNAME 仅配置了带 `www` 的地址。如果也希望通过裸域 `sensedex.online` 访问，在 DNS 管理页面额外添加下面四条 A 记录（线路均选“默认”，TTL 均可设为 `600`）：

| 主机记录 | 记录类型 | 记录值 |
| --- | --- | --- |
| `@` | `A` | `185.199.108.153` |
| `@` | `A` | `185.199.109.153` |
| `@` | `A` | `185.199.110.153` |
| `@` | `A` | `185.199.111.153` |

两者都正确配置后，GitHub Pages 会将裸域跳转到设置的主域名 `www.sensedex.online`。可在终端核对 DNS 返回值：

```sh
dig www.sensedex.online CNAME +short
# 预期：samlee1732.github.io.

# 仅在添加了上述裸域 A 记录后检查：
dig sensedex.online A +short
# 预期：上表中的四个 IP，顺序可能不同。
```

DNS 查询只用于核对解析记录，最终还需在浏览器中确认网站能通过 HTTPS 打开。操作步骤及 IP 地址可对照 [GitHub Pages 自定义域名官方说明](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)。

## 个人信息区

首页简介下方新增个人信息与联系方式，采用参考图中的逐行布局。姓名、讲师职称、机电工程学院和深圳职业技术大学的单位信息，来自作者指定的个人站点：

- http://www.senli.site/
- http://www.senli.site/index_zh.html

姓名显示为 Sen LI, Ph.D.（李森）。邮箱由作者直接提供，使用 `lisen3@szpu.edu.cn`，并让 `mailto:` 与显示地址一致。办公地址由作者直接提供，为“深圳职业技术大学西丽校区厚德楼4楼”，同时显示对应英文地址。未提供电话，页面没有添加电话。学校名称及职称已在简介和相关概览中同步统一。

## 品牌资源

- `assets/sensedex-mark.png`：透明背景的独立图形，用于页头与浏览器标签页图标。
- `assets/sensedex-logo-v2.png`：包含 SenseDex Lab、Sensing and Dexterous Manipulation 与中文名称的完整透明 Logo。

图形由内置 image_gen 工具生成；页头品牌文字使用 HTML，以保证小屏显示清晰。
