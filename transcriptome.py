#!/usr/bin/python
import sys
import os
import subprocess
args=sys.argv
def main(): 
	#import subprocess,os,sys

	print ''
	print "##############################################################################################"
	print ''
	print "   hisat2 + sam2bam + bam2sort + HTseq + RNA-edit"
	print ''
	print "   need software (hisat2 samtools htseq-count and SPRINT) ; "
	print "   need to change 'sp'(sprint_from_bam of SPRINT) and 'samtools_path(samtools path of SPRINT)'"
	print ''
	print "   https://github.com/Drbiology"
	print ''
	print "   Please contact drbiology@aliyun.com when questions arise."
	print ''
	print "##############################################################################################"   
	def help_doc():
        	print ""
        	print ""
        	print ""
        	print "   Usage:"
        	print ""
        	print "      python <script.py> id(fastq) reference_genome(.fa) fastq_path gtf_path outfile_path "
        	print ""
        	print "   Example: "
        	print ""
        	print "      python hisat.py ID \ "
		print "			/home/ref_genome/Setaria_italica.Setaria_italica_v2.0.dna.toplevel.fa \ "
		print "			/home/guzi/fastq_data/ \ "
		print "			/home/gtf/Setaria_italica.Setaria_italica_v2.0.42.gtf \ "
		print "			/home/result "
        	print ""
        	print ""
        	#print sys.argv[0]
        
		sys.exit(0)
	if len(sys.argv)<5:
        	#print sys.argv[0]
        	help_doc()
	
	##############################
	#args[1] : fastq id
	#args[2] : index file path
	#args[3] : fastq file path
	#args[4] : gtf file path
	#args[5] : outfile path
	##############################
	### hisat2 ###################
	index=args[2]
	fqdir=args[3]
	### Rna-edit #################
	rna_edit_path='Rna-edit'
	sp='./software/SPRINT/bin/sprint_from_bam'
	samtools_path='./software/SPRINT/samtools_and_bwa/samtools'	### samtools of SPRINT
	### HTseq ####################
	gtf=args[4]
	
	def hisat2(index,fqdir,sample_id):
		return os.system('hisat2 -x {0} \
		-p 8 \
		-1 {1}/{2}_r1.fq \
		-2 {1}/{2}_r2.fq \
		-S {2}.sam \
		1>{2}.log \
		2>{2}.align.summary.txt'.format(index,fqdir,sample_id))
	
	def samtools(sample_id):
		sam2bam=os.system('samtools view \
			-Sbh {0}.sam \
			> {0}.bam'.format(sample_id))
		bam2sort=os.system('samtools sort {0}.bam \
			{0}.sort'.format(sample_id))
		return sam2bam;return bam2sort

	def sprint(sp,sample_id,index,out_path,samtools_path):
		os.mkdir(out_path)
		return os.system('{0} {1}.bam {2} {3} {4}' \
				.format(sp,sample_id,index,rna_edit_path,samtools_path))

	def htseq(sample_id,gtf):
		return os.system('htseq-count -f bam {0}.sort.bam \
				{1} > {0}_count_number.txt'.format(sample_id,gtf))
	
	def bedtools(gtf,line):
		return os.system('bedtools -intersect \
				-a SPRINT_identified_regular.res \
				-b {0} \
				-wb >{1}_edit_annotation'.format(gtf,line))
	
	#f=open(args[1],'r')
	old_path=os.getcwd()
	path=args[5]+'/'
	
	for line in open(args[1],'r'):
		line=line.rstrip('\n');sample_id = line
		os.chdir(path);os.makedirs(path+line);os.chdir(path+line)	### Create working directory and enter it
		hisat2(index,fqdir,sample_id);samtools(sample_id);htseq(sample_id,gtf)
		sprint(sp,sample_id,index,rna_edit_path,samtools_path)
		os.chdir(rna_edit_path);bedtools(gtf,line)
		os.chdir(old_path)

     
     	f.close()
	


main()


if __init__ == 'main':
	main()




