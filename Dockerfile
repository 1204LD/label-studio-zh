ARG BASE_IMAGE=heartexlabs/label-studio:1.23.0
FROM ${BASE_IMAGE}

# 汉化补丁：仅替换前端构建产物中的界面文案与 Django 模板中的文字，
# 不修改后端逻辑、数据库结构或依赖版本。
COPY --chown=1001:0 scripts /label-studio/.ls-zh/scripts
COPY --chown=1001:0 dict /label-studio/.ls-zh/dict

RUN python /label-studio/.ls-zh/scripts/patch_bundles_global.py /label-studio/web/dist /label-studio/.ls-zh/dict/zh-CN.json \
 && python /label-studio/.ls-zh/scripts/patch_bundles_context.py /label-studio/web/dist /label-studio/.ls-zh/dict/zh-CN-context.json \
 && python /label-studio/.ls-zh/scripts/patch_templates.py /label-studio/label_studio /label-studio/.ls-zh/dict/zh-CN-templates.json \
 && rm -rf /label-studio/.ls-zh

LABEL org.opencontainers.image.title="Label Studio 简体中文汉化版" \
      org.opencontainers.image.description="Label Studio 1.23.0 的前端中文汉化补丁镜像" \
      org.opencontainers.image.source="https://github.com/1204LD/label-studio-zh" \
      org.opencontainers.image.licenses="Apache-2.0"

# 保持与官方镜像一致
ENV LABEL_STUDIO_DISABLE_UPDATE_CHECK=true
