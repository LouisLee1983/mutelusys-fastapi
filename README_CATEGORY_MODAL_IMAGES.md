# 编辑分类弹窗中图片显示功能实现文档

## 功能概述

实现了编辑分类弹窗中的图片展示功能，包括当前图片的显示、删除和上传新图片的完整流程。

## 实现功能

### 1. 当前图片展示

**分类大图显示：**
- 尺寸：200x120 像素
- 显示当前分类的大图
- 提供删除功能
- 支持图片预览

**分类图标显示：**
- 尺寸：80x80 像素
- 显示当前分类的图标
- 提供删除功能
- 支持图片预览

### 2. 交互功能

**图片上传：**
- 支持拖拽上传
- 实时显示上传进度
- 文件格式验证（JPG、PNG、WebP、GIF）
- 文件大小限制（最大10MB）

**图片删除：**
- 确认对话框防止误操作
- 删除后自动刷新显示
- 删除后使用默认图片

**状态显示：**
- 上传中显示 Loading 状态
- 有图片时显示"更换"按钮
- 无图片时显示"上传"按钮

### 3. UI/UX 优化

**视觉设计：**
- 使用虚线边框区分图片区域
- 鼠标悬停时边框颜色变化
- 统一的圆角和阴影效果
- 清晰的图片标签说明

**交互反馈：**
- 操作成功/失败的消息提示
- 确认删除的二次确认
- 上传进度的实时显示

## 关键代码实现

### 1. 图片URL处理

```typescript
// 处理图片URL的工具函数
const getImageUrl = (imageUrl: string | null | undefined): string | undefined => {
  if (!imageUrl) return undefined;
  
  // 如果已经是完整URL，直接返回
  if (imageUrl.startsWith('http://') || imageUrl.startsWith('https://')) {
    return imageUrl;
  }
  
  // 如果是相对路径，拼接MEDIA_URL
  if (imageUrl.startsWith('/static/')) {
    return `${MEDIA_URL}${imageUrl.substring(7)}`; // 去掉/static/前缀
  }
  
  // 如果是其他相对路径，直接拼接
  return `${MEDIA_URL}/${imageUrl}`;
};
```

### 2. 图片显示组件

```typescript
{selectedCategory?.image_url ? (
  <div className="mb-4">
    <div className="border-2 border-dashed border-gray-200 rounded-lg p-4 bg-gray-50 hover:border-blue-300 transition-colors">
      <div className="text-center">
        <div className="mb-2">
          <Text type="secondary" className="text-sm">当前大图</Text>
        </div>
        <Image
          width={200}
          height={120}
          src={getImageUrl(selectedCategory.image_url)}
          alt="当前分类大图"
          style={{ objectFit: 'cover', borderRadius: '8px', border: '1px solid #f0f0f0' }}
          fallback="data:image/png;base64,..."
        />
        <div className="mt-3">
          <Popconfirm
            title="确定删除当前大图吗？"
            description="删除后将使用默认图片"
            onConfirm={() => handleDeleteImage('hero')}
            okText="确定"
            cancelText="取消"
          >
            <Button size="small" danger icon={<DeleteOutlined />}>
              删除大图
            </Button>
          </Popconfirm>
        </div>
      </div>
    </div>
  </div>
) : null}
```

### 3. 上传组件

```typescript
<Upload
  {...heroUploadProps}
  listType="picture-card"
  maxCount={1}
  showUploadList={false}
>
  <div>
    {heroImageUploading ? <LoadingOutlined /> : <UploadOutlined />}
    <div className="mt-2">
      {heroImageUploading ? '上传中...' : (selectedCategory?.image_url ? '更换大图' : '上传大图')}
    </div>
  </div>
</Upload>
```

## 状态管理

### 1. 图片状态同步

**上传成功后：**
1. 重新加载分类数据
2. 更新selectedCategory状态
3. 自动刷新Modal中的图片显示

**删除成功后：**
1. 重新加载分类数据
2. 更新selectedCategory状态
3. 自动刷新Modal中的图片显示

### 2. 加载状态管理

```typescript
const [heroImageUploading, setHeroImageUploading] = useState(false);
const [iconImageUploading, setIconImageUploading] = useState(false);
```

## 用户交互流程

### 1. 编辑现有分类

1. 用户选择分类后点击"编辑"按钮
2. 打开编辑Modal，切换到"媒体信息"标签
3. 显示当前分类的大图和图标（如果有）
4. 用户可以：
   - 查看当前图片
   - 删除现有图片
   - 上传新图片
   - 更换现有图片

### 2. 创建新分类

1. 用户点击"添加分类"按钮
2. 打开创建Modal，切换到"媒体信息"标签
3. 显示空的上传区域
4. 用户可以上传分类的大图和图标

## 错误处理

### 1. 文件验证

- 检查文件格式是否支持
- 检查文件大小是否超限
- 显示具体的错误提示

### 2. 网络错误

- 上传失败时显示错误消息
- 网络超时处理
- 自动重试机制

### 3. 权限错误

- 检查用户权限
- 显示权限不足提示

## 性能优化

### 1. 图片加载优化

- 使用Antd Image组件的懒加载
- 提供fallback图片
- 图片压缩和优化

### 2. 状态更新优化

- 避免不必要的重新渲染
- 使用useCallback优化函数
- 合理的状态管理

## 测试场景

### 1. 功能测试

- ✅ 显示现有分类的图片
- ✅ 上传新图片
- ✅ 删除现有图片
- ✅ 更换图片
- ✅ 文件格式验证
- ✅ 文件大小验证

### 2. UI测试

- ✅ 图片正确显示
- ✅ 按钮状态正确
- ✅ 加载状态显示
- ✅ 错误提示显示
- ✅ 响应式布局

### 3. 兼容性测试

- ✅ 不同浏览器兼容
- ✅ 不同图片格式支持
- ✅ 移动端适配

## 注意事项

1. **图片路径处理：** 确保正确拼接MEDIA_URL
2. **状态同步：** 上传/删除后及时更新UI
3. **错误处理：** 提供友好的错误提示
4. **性能考虑：** 避免大文件上传影响用户体验
5. **用户体验：** 提供清晰的操作指引和反馈

## 未来改进

1. **批量上传：** 支持同时上传多张图片
2. **图片编辑：** 在线裁剪和调整
3. **预设模板：** 提供常用图片模板
4. **智能推荐：** 根据分类自动推荐合适图片
5. **CDN集成：** 支持CDN存储和加速 