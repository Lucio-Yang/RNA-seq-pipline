#!/usr/bin/python
import sys
import os
import shutil
args=sys.argv

fastq_path=args[1]
tri_path='./Trimmomatic-0.38/trimmomatic-0.38.jar'
old_path=os.getcwd()

class sra():
	
	def __init__(self,id,tri_path):
		self.id = id
		self.tri_path=tri_path

	def sra2fastq(self):
		return os.system('fastq-dump --split-files {0}.sra'.format(self.id))
	
	def trimmomatic(self):
		self.tri_path=tri_path
		return os.system("java -jar {1} PE -threads 4 \
			{0}_1.fastq {0}_2.fastq \
			{0}_1.P.fq {0}_1.UP.fq \
			{0}_2.P.fq {0}_2.UP.fq \
			HEADCROP:18 MINLEN:50 TOPHRED33".format(self.id,self.tri_path))
	
	def move(self):
		try :
			shutil.move('{0}.sra'.format(self.id), 'sra')
			shutil.move('{0}_1.fastq'.format(self.id), 'fastq')
			shutil.move('{0}_2.fastq'.format(self.id), 'fastq')
			shutil.move('{0}_1.UP.fq'.format(self.id), 'trimmomatic')
			shutil.move('{0}_2.UP.fq'.format(self.id), 'trimmomatic')
			shutil.move('{0}_1.P.fq'.format(self.id), 'data')
			shutil.move('{0}_2.P.fq'.format(self.id), 'data')
		except IOError:
			pass
def id():
	return os.system("ls | sed 's/.sra//p' | uniq | sed 's/id//p' > id")

def mkdir():
	return os.system('mkdir -p fastq sra trimmomatic data result')
		
os.chdir(fastq_path);id();mkdir()
for i in open('id','r'):	
	i = i.rstrip('\n')
	sra(i,tri_path).sra2fastq()
	sra(i,tri_path).trimmomatic()
	sra(i,tri_path).move()
os.chdir(old_path)

if __name__ == 'main':
	main()
