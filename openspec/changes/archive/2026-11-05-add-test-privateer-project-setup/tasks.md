# Tasks

## 1. 建立项目 Setup

- [x] 1.1 新增 `skills/setup-test-privateer/SKILL.md`，实现调查、建议、逐项确认、草稿预览、写入和回读流程，并用契约测试验证不会运行测试、安装或擅自选择框架、配置模型，或把配置保存误报为环境已验证
- [x] 1.2 新增 `skills/setup-test-privateer/references/project-profile-template.md`，定义 `.test-privateer/project.md` 的受管区、来源指针、测试表面与框架约定和必要章节，并验证模板不复制 TCO、用例或秘密值
- [x] 1.3 新增文件维护契约测试，使用临时项目副本验证初次写入、幂等重跑、人工内容保留、失效来源更新和回读失败边界

## 2. 接入 Test Privateer 路由

- [x] 2.1 更新 `skills/test-privateer/SKILL.md`，将明确初始化请求路由到 `setup-test-privateer`，并验证普通项目任务在没有配置时仍可继续
- [x] 2.2 更新 `skills/test-privateer/references/artifact-routing.md`，说明项目配置、TCO、需求资产和 Run 资产的职责与优先级，并用契约测试检查 TCO 资源入口只被引用、不被项目配置复制
- [x] 2.3 更新 Skill 包完整性和入口测试，验证新 Skill、引用和模板可以从主入口到达，项目配置冲突会触发澄清而不是静默覆盖，且框架专项只在项目明确选择对应框架时加载

## 3. 验证真实行为

- [x] 3.1 新增 `evals/project-test-setup/` 的自然输入和判据，覆盖已有项目规则、缺少环境决定、无 TCO、重复运行、秘密信息、回读差异、项目已选框架、自有 Agent 评测框架、无配置普通任务和配置冲突
- [x] 3.2 按现有协议运行真实模型行为评测，记录完整输出、Skill 加载轨迹、文件差异和失败边界，并将原始记录保存到 `.local/validation/project-test-setup/`
- [x] 3.3 根据评测修正 Setup 和模板后，运行 `python3 -m unittest discover -s tests -v`、`python3 scripts/check_skill_package.py`、`openspec validate add-test-privateer-project-setup --strict --no-interactive`、`openspec validate --all --strict --no-interactive` 和 `git diff --check`
- [x] 3.4 交付实现、评测范围和剩余风险，保留活动 change，等待用户明确确认后再同步规格和归档
