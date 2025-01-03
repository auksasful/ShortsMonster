from modules.base_generator import BaseGenerator


class ScriptDivider(BaseGenerator):
    def __init__(self, project_folder):
        # Call the constructor of the base class
        super().__init__(project_folder)

    def execute(self):
        data = self.read_csv(self.script_file_path)

        # print(data)
        print(data[0][0]['Scene'])