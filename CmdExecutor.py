import subprocess

class CmdExecutor:
	def ExecuteCommand(self, cmd):
		cmd = "adb " + cmd
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		return output