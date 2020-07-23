from django.contrib import admin
from .models import Article,Device,Device_Data
# Register your models here.
admin.site.site_header = '设备管理后台'
admin.site.site_title = '设备管理后台'
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_time', 'riqi')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # ordering设置默认排序字段，负号表示降序排序
    # ordering = ('-created_time',)

    # list_editable 设置默认可编辑字段，在列表里就可以编辑
    # list_editable = ['title', 'user']

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'title')

    # fk_fields 设置显示外键字段
    # fk_fields = ['category']

    #列表顶部，设置为False不在顶部显示，默认为True。
    # actions_on_top=True

    #列表底部，设置为False不在底部显示，默认为False。
    # actions_on_bottom=False

    # 定制Action行为具体方法
    # def func(self, request, queryset):
    #     queryset.update(created_time='2018-09-28')
        # 批量更新我们的created_time字段的值为2018-09-28

    # func.short_description = "中文显示自定义Actions"
    # actions = [func, ]

    search_fields = ['title']

@admin.register(Device_Data)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'power', 'created_time',)
    list_display_links = ('device',)

class DeviceDataInline(admin.StackedInline):
    # 继承HeroInfo
    model = Device_Data
    # 嵌入3个form表单
    extra = 0

class DeviceAdmin(admin.ModelAdmin):
    list_display = ( 'deviceID', 'info', 'created_time',)
    list_display_links = ('deviceID',)
    # 嵌入
    inlines = [DeviceDataInline]

admin.site.register(Device, DeviceAdmin)