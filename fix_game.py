# -*- coding: utf-8 -*-
"""修复灰域行者游戏：添加场景6，重新排列场景顺序"""

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 场景6的内容（药效+治疗，上午9:00，中度压抑）
scene6 = '''
  // ---- SCENE 6 ----
  {
    id:6, name:"药效", location:"上午 9:00 · 治疗室",
    narrative:"治疗结束后，你坐在椅子上休息。药效开始起作用了。\n\n那些声音变得……遥远了一些。像是隔着一层厚厚的玻璃，还在说话，但你不那么在意了。\n\n治疗师走进来，在你对面坐下：「昨晚怎么样？今天感觉如何？」",
    voices:[
      {persona:"inland",delay:1500,pos:{left:"5%",top:"15%"},repeat:true},
      {persona:"volition",delay:3000,pos:{right:"5%",top:"20%"},repeat:false},
      {persona:"logic",delay:4500,pos:{left:"8%",bottom:"25%"},repeat:false}
    ],
    glitchLevel:2,
    hallEffect:null,
    choices:[
      {letter:"A",text:"和治疗师分享你的感受",effect:"开放沟通 · 建立信任",
        outcome:"你告诉治疗师，昨晚声音很吵，但现在……好多了。治疗师点点头：「药效通常会持续4-6小时。你做得很好，愿意来治疗。」",
        voices:[{persona:"empathy",text:"你愿意分享，这本身就是进步。"},{persona:"volition",text:"治疗师在听。你被看见了。"}],
        therapistNote:"开放沟通是治疗的核心。治疗师：你觉得和治疗师分享感受，和告诉家人有什么不同？你有没有觉得有些话只能对治疗师说？"},
      {letter:"B",text:"询问药物的作用机制",effect:"认知理解 · 减少恐惧",
        outcome:"治疗师解释：「这种药物作用于多巴胺受体，帮助大脑减少异常信号。它不是让声音消失，而是让你不那么受它们影响。」",
        voices:[{persona:"logic",text:"多巴胺D2受体拮抗剂。科学原理。你可以理解它。"},{persona:"volition",text:"知道原理，你就不会被它控制。"}],
        therapistNote:"理解药物原理可以帮助减少对未知的恐惧。治疗师：你对药物有什么担心吗？有没有想过停药？对于精分患者，药物治疗通常是必要的，但需要长期坚持。"},
      {letter:"C",text:"安静地坐着，感受药效",effect:"自我觉察 · 内心平静",
        outcome:"你闭上眼睛，静静感受。声音还在，但像远处的海浪——有节奏，但不刺耳。你感到一种久违的平静。",
        voices:[{persona:"volition",text:"平静。你找到了它。"},{persona:"inland",text:"……它们在墙角看着你，但它们不说话了。"}],
        therapistNote:"自我觉察是疗愈的重要能力。治疗师：你描述声音像「远处的海浪」，这个比喻很好。你有没有发现，当你不与声音对抗时，它们反而变得更温和？"}
    ],
    therapist:{
      title:"场景六 · 治疗观察点",
      text:"药效是治疗过程中的重要环节。药物不是让症状消失，而是让患者有能力应对它们。这个场景展示了药物起效时的体验——声音还在，但变得可管理。关键是：药物+心理治疗的效果远好于单一治疗。",
      questions:["你对药物有什么感觉？","你觉得和治疗师的沟通怎么样？","你现在对声音的态度有什么变化？"]
    }
  },
'''

# 找到SCENES数组的位置
scenes_start = content.find('var SCENES = [')
if scenes_start == -1:
    print("错误：找不到SCENES数组")
    exit(1)

# 找到场景1的结束位置（id:1的场景对象结束的}）
# 我们需要在场景1之后插入场景6

# 使用正则表达式找到每个场景
import re

# 找到所有场景的id
scene_pattern = r'\{id:(\d+),'
scene_matches = list(re.finditer(scene_pattern, content))
print(f"找到场景: {[m.group(1) for m in scene_matches]}")

# 找到场景1的位置
scene1_start = None
for m in scene_matches:
    if m.group(1) == '1':
        scene1_start = m.start()
        break

if not scene1_start:
    print("错误：找不到场景1")
    exit(1)

# 找到场景1的结束位置（下一个场景开始之前，或者场景1的}后跟逗号）
# 我们需要找到场景1的完整对象

# 从场景1开始，找到匹配的}
brace_count = 0
in_scene1 = False
scene1_end = None

for i in range(scene1_start, len(content)):
    if content[i] == '{':
        brace_count += 1
        in_scene1 = True
    elif content[i] == '}':
        brace_count -= 1
        if in_scene1 and brace_count == 0:
            scene1_end = i + 1
            break

if not scene1_end:
    print("错误：无法找到场景1的结束位置")
    exit(1)

print(f"场景1位置: {scene1_start} - {scene1_end}")

# 检查场景1后面是否有逗号
has_comma = content[scene1_end] == ','

# 构建新内容
# 在场景1之后插入场景6
if has_comma:
    # 场景1后面已经有逗号，直接插入场景6
    new_content = content[:scene1_end] + '\n' + scene6 + content[scene1_end+1:]
else:
    # 场景1后面没有逗号，添加逗号后插入场景6
    new_content = content[:scene1_end] + ',\n' + scene6 + content[scene1_end:]

# 修复语法错误：移除多余的逗号（},// ---- SCENE 4 ----）
new_content = new_content.replace('},\n\n  ,// ---- SCENE 4 ----', '},\n\n  // ---- SCENE 4 ----')

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("修复完成！场景6已添加")

# 验证
with open('index.html', 'r', encoding='utf-8') as f:
    verify_content = f.read()

verify_matches = list(re.finditer(scene_pattern, verify_content))
print(f"验证 - 找到场景: {[m.group(1) for m in verify_matches]}")
