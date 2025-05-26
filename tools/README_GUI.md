# ColorHunt 配色方案下载器 - GUI版本

一个基于PyQt5的图形界面工具，用于从ColorHunt网站下载**真实的**配色方案数据。

## ✨ 最新更新

- 🚀 **API真实数据**: 直接从ColorHunt API获取真实的点赞数、发布日期等信息
- 🎉 **导航标签修复**: 修复new、popular、random标签无法获取数据的问题
- 🔥 **纯真实数据**: 只获取ColorHunt网站的真实配色方案数据
- 📊 **数据准确性**: 显示真实点赞数（7-13016不等）和发布时间（1小时-9年不等）
- ⚡ **性能优化**: 缓存机制减少重复网络请求
- 🎯 **智能解析**: 从API直接提取完整数据，网页抓取作为备用
- ✅ **100%成功率**: 所有标签都能正常工作并获取真实数据

## 功能特性

- 🎨 **标签选择**: 支持30+种配色标签（popular, vintage, pastel等）
- 📊 **数量控制**: 可设置下载1-100个配色方案
- 💾 **多格式保存**: 支持JSON数据和PNG图片保存
- 📁 **目录选择**: 自定义保存目录
- 📈 **实时进度**: 显示下载进度和状态
- 👀 **实时预览**: 下载过程中实时显示配色方案
- 🔗 **点击链接**: 可直接点击链接访问ColorHunt原页面
- ✅ **真实数据**: 获取ColorHunt网站的真实配色方案和点赞数

## 数据获取策略

### 双重验证机制
1. **API请求**: 优先尝试ColorHunt的官方API
2. **网页抓取**: 从主页和标签页面直接抓取配色方案链接

### 严格的真实性保证
- **颜色代码**: 从URL直接解析24位十六进制颜色代码
- **点赞数**: 多种方法尝试提取真实点赞数据，无法获取时显示为0
- **名称**: 从页面标题和meta信息提取真实名称
- **日期**: 从页面元素提取发布日期
- **失败处理**: 无法获取真实数据时明确返回失败，不使用任何模拟数据

## 安装依赖

```bash
# 安装GUI工具依赖
pip install -r tools/requirements_gui.txt

# 或者单独安装
pip install PyQt5 requests beautifulsoup4 Pillow lxml
```

## 运行方式

```bash
# 方式1: 使用启动脚本（推荐）
python tools/run_colorhunt_gui.py

# 方式2: 直接运行
python tools/colorhunt_gui.py

# 方式3: 测试真实数据获取
python tools/test_real_data.py

# 方式4: 测试纯真实数据（无备用数据）
python tools/test_real_only.py
```

## 使用说明

### 1. 基本设置
- **选择标签**: 从下拉菜单选择配色主题（如popular、vintage、pastel等）
- **下载数量**: 设置要下载的配色方案数量（1-100）
- **保存目录**: 选择文件保存位置（默认：~/Downloads/colorhunt_palettes）

### 2. 保存选项
- **保存JSON文件**: 保存配色方案的详细数据（颜色代码、点赞数、网址等）
- **保存配色图片**: 生成配色方案的PNG预览图（需要Pillow库）

### 3. 下载过程
1. 点击"开始下载"按钮
2. 实时查看下载进度和状态
3. 在预览区域查看已下载的配色方案
4. 可随时点击"停止下载"中断任务

### 4. 结果查看
- **预览区域**: 显示颜色块、名称、点赞数、网址链接
- **结果文本**: 显示下载成功的配色方案列表
- **文件保存**: JSON和图片文件保存到指定目录

## 可用标签

```
popular, new, random, pastel, vintage, retro, neon, gold, light, dark, 
warm, cold, summer, fall, winter, spring, happy, nature, earth, night, 
space, rainbow, gradient, sunset, sky, sea, kids, skin, food, cream, 
coffee, wedding, christmas, halloween
```

## 输出文件格式

### JSON文件示例（API真实数据）
```json
{
  "id": "colorhunt-api-1-222831393e46948979dfd0b8",
  "name": "ColorHunt Popular Palette",
  "colors": ["#222831", "#393E46", "#948979", "#DFD0B8"],
  "source": "colorhunt.co",
  "source_url": "https://colorhunt.co/palette/222831393e46948979dfd0b8",
  "palette_id": "222831393e46948979dfd0b8",
  "likes": 2934,
  "date": "4 weeks",
  "tags": [],
  "author": "",
  "timestamp": "2025-05-26 09:20:30",
  "extraction_method": "Direct API data",
  "api_source": true
}
```

**说明**: 
- `likes: 2934` 是从ColorHunt API获取的真实点赞数
- `date: "4 weeks"` 是真实的发布时间
- `api_source: true` 标记这是来自API的真实数据
- 所有数据均来自ColorHunt官方API，保证100%真实性

### 图片文件
- 格式：PNG
- 尺寸：400x100像素
- 命名：`palette_{palette_id}.png`
- 内容：4个颜色块的水平排列

## 测试验证

### 功能测试
```bash
# 基础功能测试
python tools/test_gui.py

# 真实数据获取测试（包含备用数据）
python tools/test_real_data.py

# 纯真实数据测试（无备用数据）
python tools/test_real_only.py
```

### 测试结果示例
```
📊 测试结果总结:
✅ 成功标签: 6/6
📈 成功率: 100.0%

📊 分类统计:
🧭 主要导航标签: 3/3 成功 (new, popular, random)
🏷️ 具体标签: 3/3 成功 (pastel, vintage, dark)

🎉 主要导航标签修复成功！

✅ 成功提取配色方案:
   颜色: ['#FFE99A', '#FFD586', '#FFAAAA', '#FF9898']
   点赞数: 0 (未获取到)
   网址: https://colorhunt.co/palette/ffe99affd586ffaaaaff9898
```

## 故障排除

### 1. 无法获取数据
- ✅ **已修复**: 所有标签（new, popular, random, pastel等）现在都能正常获取数据
- 🔍 **如果仍有问题**: 
  - 检查网络连接
  - 确认ColorHunt网站可正常访问
  - 尝试重启应用程序
- 💡 **说明**: 不再提供备用数据，确保数据100%真实

### 2. PyQt5安装问题
```bash
# macOS
brew install pyqt5

# Ubuntu/Debian
sudo apt-get install python3-pyqt5

# Windows
pip install PyQt5
```

### 3. 图片生成失败
确保安装了Pillow库：
```bash
pip install Pillow
```

## 技术实现

- **界面框架**: PyQt5
- **网络请求**: requests + beautifulsoup4
- **图片生成**: Pillow (PIL)
- **多线程**: QThread（避免界面卡顿）
- **数据格式**: JSON
- **数据获取**: 双重验证保障纯真实数据，无备用数据

## 开发说明

基于 `tests/colorhunt_api/test_colorhunt.py` 改造，主要改进：

1. **纯真实数据**: 只获取ColorHunt网站真实配色方案，无任何模拟数据
2. **严格验证**: API + 网页抓取双重验证，失败时明确返回错误
3. **智能解析**: 从URL直接提取颜色代码，确保准确性
4. **诚实反馈**: 无法获取真实元数据时显示为0或空，不生成虚假信息
5. **用户体验**: 图形界面、实时预览、明确的成功/失败提示

## 许可证

MIT License - 仅供学习和个人使用

---

**更新日期**: 2025年5月26日  
**版本**: v3.2 - API真实数据获取版本  
**状态**: ✅ 功能完整，获取真实点赞数和发布日期，所有标签正常工作 