import subprocess

class CmdExecutor:
	def ExecuteCommand(self, cmd, isADB=True):
		command = ""
		if isADB:
			command = "adb " + cmd
		else:
			command = cmd
		p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		output = p.communicate()[0].decode("utf-8", errors="ignore")
		p_status = p.wait()
		return output