import os

from ClassWidgets.SDK import CW2Plugin, PluginAPI


class ExamplePlugin(CW2Plugin):
    def on_load(self):
        super().on_load()
        print(self.api.ui.register_settings_page(
            title='Settings',
            qml_path=os.path.join(os.path.dirname(__file__), 'settings.qml'),
            plugin=self,
        ))


if __name__ == '__main__':
    plugin = ExamplePlugin(PluginAPI(None))
    plugin.on_load()