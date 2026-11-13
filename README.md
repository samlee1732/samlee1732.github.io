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
- `assets/main.js`：手机菜单、Teaching 下拉菜单和信息弹窗。

页面视觉参考用户提供的截图。中英文简介按作者新提供的个人经历更新，英文为对应译文；中文修正了“EEE → IEEE”和“2026毕业 → 2026年毕业”两处笔误，并依据作者个人站点统一了职称与学校名称。履历、论文数量及项目经历由作者提供，未做外部核实。

目前交付范围是首页。Publication 导航跳转到联系方式下方的论文展示区；Team 展示作者提供的概览信息，完整论文与成员名单仍需补充；Teaching 展示《机器人学及应用》和《自动控制原理》两门课程，课程资料仍需补充。右上角 Contact 链接跳转到个人信息与联系方式；手机端点击页内导航后会先收起导航菜单。网站采用玫红、紫色到深蓝的渐变，实验室标题、导航选中线、Contact 按钮与图标保持一致。

顶部导航的 News 位于 Teaching 之后，跳转到页面下方的 `#news` 动态区。目前显示待更新提示；后续在 `index.html` 的该区域替换为真实的日期和动态内容即可。窄屏导航在 1000px 及以下收进菜单，点击 News 会收起菜单并跳转。

## 补充论文与素材

`index.html` 的 `#publication` 区域按“左侧论文信息、右侧图片或视频”排版，手机端改为上下排列。目前录入的 ActiveSPN 作者、题目、刊物、卷期页码、年份和 Accepted 状态均来自作者提供的截图；没有添加未提供的 DOI、摘要或引用数据。

- 新增论文：复制 `.publication-list` 下的一个 `<li>`，修改作者、标题和发表信息，并同步修改标题的 `id` 与文章的 `aria-labelledby`，保持 ID 唯一。编号会自动生成。
- 补图片：将素材放入 `assets/publications/`（需要时创建），用带有准确 `alt` 描述的 `<img src="./assets/publications/文件名.png" alt="论文方法示意图的描述" loading="lazy">` 替换 `.publication-placeholder`。
- 补视频：在同一位置使用 `<video controls preload="metadata" src="./assets/publications/文件名.mp4"></video>`；有封面时可增加 `poster` 属性。
- 补资料：将 Abstract、Links、BibTeX 的不可点击占位文字替换为对应的真实链接或有实际内容的展开区。资料齐全后删除该论文的 “Materials coming soon” 提示。

## 本项目的部署位置

- 仓库：https://github.com/samlee1732/samlee1732.github.io
- 主页：https://samlee1732.github.io/
- 发布来源：`main` 分支的仓库根目录（`/`）。

推送到 `main` 后，GitHub Pages 自动发布更新。部署进度可在仓库的 Actions 或 Settings → Pages 查看。

## 购买域名后的解析与绑定

以 `sensedex.online` 为例，下面的配置将 `www.sensedex.online` 绑定到本项目的 GitHub Pages。

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
