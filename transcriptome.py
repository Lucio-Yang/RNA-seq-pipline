#!/usr/bin/python
import sys
import os
import subprocess
args=sys.argv

def help():
    '''
    ##################################################################################################
	
        Hisat2 + Sam2Bam + Bam2Sort + Stringtie(Htseq) + RNA-edit + Bedtools
	
        need hisat2 samtools htseq-count and SPRINT ;
        need to change 'sp'(sprint_from_bam of SPRINT) and 'samtools_path'(samtools path of SPRINT)
	
        https://github.com/Drbiology
	
        Please contact drbiology@aliyun.com when questions arise.
	
    ##################################################################################################
	
      Usage:
	
        python transcriptome.py id(fastq_id) reference_genome(.fa) fastq_path gtf_path outfile_path
	
      Example:
	
        python transcriptome.py ID /home/ref_genome/<>.fa /home/fastq_data/ /home/<>.gtf /home/result
    
    ##################################################################################################
	
    '''

def main():
	
    ##############################
    #args[1] : fastq id
    #args[2] : index file path
    #args[3] : fastq file path
    #args[4] : gtf file path
    #args[5] : outfile path
    #############################
	
    index=args[2]
    fqdir=args[3]
    gtf=args[4]

    rna_edit_path='Rna-edit'
    sp='/home/software/SPRINT/bin/sprint_from_bam'
    samtools_path='/home/software/SPRINT/samtools_and_bwa/samtools'	### samtools of SPRINT
	
    def hisat2(index,fqdir,sample_id):        ### used '-U {1}/{2}_1.p.fq' for single-ended
        return os.system('hisat2 -x {0} \
            -p 8 \
            -1 {1}/{2}_1.P.fq \
            -2 {1}/{2}_2.P.fq \
            -S {2}.sam \
             1>{2}.log \
             2>{2}.align.summary.txt'.format(index,fqdir,sample_id))
	
    def samtools(sample_id):
        sam2bam=os.system('samtools view \
            -Sbh {0}.sam -o {0}.bam'.format(sample_id))
        bam2sort=os.system('samtools sort {0}.bam -T {0} \
            -o {0}.sort.bam'.format(sample_id))
        return sam2bam; return bam2sort
	
    def sprint(sp,sample_id,index,out_path,samtools_path):
        os.mkdir(out_path)
        return os.system('{0} {1}.bam {2} {3} {4}' \
            .format(sp,sample_id,index,rna_edit_path,samtools_path))
	
    def stringtie(sample_id,gtf):
        return os.system('stringtie {0}.sort.bam -o {0}.gtf -p 16 -G {1} \
            -A gene_abund.tab -B -e '.format(sample_id,gtf))
		
    def htseq(sample_id,gtf):
        return os.system('htseq-count -f bam {0}.sort.bam \
            {1} > {0}_count_number.txt'.format(sample_id,gtf))
	
    def bedtools(gtf,line):
        return os.system('bedtools intersect \
            -a SPRINT_identified_regular.res \
            -b {0} \
            -wb >{1}_edit_annotation'.format(gtf,line))
	
    old_path=os.getcwd()
    path=args[5]+'/'
		
    for line in open(args[1],'r'):
        line=line.replace('\n','');sample_id = line
        os.chdir(path); os.makedirs(path+line); os.chdir(path+line)	### Create working directory and enter it
        hisat2(index,fqdir,sample_id); samtools(sample_id)
        stringtie(sample_id,gtf); htseq(sample_id,gtf)
        sprint(sp,sample_id,index,rna_edit_path,samtools_path)
        os.chdir(rna_edit_path);bedtools(gtf,line)
        os.chdir(old_path)
	
    f.close()
		
if len(sys.argv)<2:
    print(help.__doc__)

if __name__ == '__main__':	
    try:
        main()
    except OSError as reason:
        print('Please input correct files. {0}'.format(reason))
    except IndexError as reason:
        print('Please input correct files. {0}'.format(reason))
	
# print("Life is short, python is shore")

