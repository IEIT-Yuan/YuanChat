### 警报

警报是基于块引用语法的 Markdown 扩展，可用于强调关键信息。 在 GitHub 上，它们以独特的颜色和图标显示，以指示内容的显著性。

只有在对用户成功至关重要时才使用警报，并将每篇文章的警报限制在一到两个，以防止读者负担过重。 此外，应避免连续发出警报。 警报无法嵌套在其他元素中。

要添加警报，请使用指定警报类型的特殊块引用行，然后在标准块引用中添加警报信息。 可以使用以下五种类型的警报：

示例:
```markdown
> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily. 

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
```
效果:
[!NOTE]
Useful information that users should know, even when skimming content.

[!TIP]
Helpful advice for doing things better or more easily. 

[!IMPORTANT]
Key information users need to know to achieve their goal.

[!WARNING]
Urgent info that needs immediate user attention to avoid problems.

[!CAUTION]
Advises about risks or negative outcomes of certain actions.