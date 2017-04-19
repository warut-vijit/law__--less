import metapy
import os
import shutil
from tokenizer import *
from graph_builder import *
from os import listdir
from os.path import isfile, join
import sys
from sklearn.preprocessing import normalize



def get_scores_for_doc(q):
	#converts sentances written to the doc.dat file by the tokenizer to an inverted index
	print os.getcwd()
	if'summarizer/' in os.getcwd():
		print "hi"
		os.chdir('summarizer/')
	onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
	#print onlyfiles
	if(os.path.exists('idx')):
		shutil.rmtree('idx')
	idx = metapy.index.make_inverted_index('config.toml')

	ranker = metapy.index.OkapiBM25()
	#rocchio = metapy.index.Rocchio(fwd)
	
	query = metapy.index.Document()
	query.content(str(q))
	print(query.content())

	results = ranker.score(idx, query, idx.num_docs())
	print('got scores from ranker')
	results = sorted(results, key = lambda doc : int(doc[0]))
	return results


def update_topic_weights(adj_matrix, sen_weights, alpha):
	print sys._getframe().f_code.co_name
	print adj_matrix

	#supplement cols
	col_height = len(adj_matrix[:,0])
	for i in xrange(len(sen_weights)):
		print (i, sen_weights[i])
		x = np.tile(sen_weights[i][1] * alpha, col_height)
		adj_matrix[:,int(sen_weights[i][1])] += x
	
	#supplement rows
	row_length = len(adj_matrix[0])
	for j in xrange(len(sen_weights)):
		#print (i, sen_weights[i])
		x = np.tile(sen_weights[j][1] * alpha, row_length)
		#print x
		adj_matrix[int(sen_weights[j][1])] += x

	print adj_matrix

	#normalize
	normed_matrix = normalize(adj_matrix, axis=1, norm='l1')
	print normed_matrix
	return normed_matrix


def update_graph_with_query(adj_matrix, query):
	sen_weights = get_scores_for_doc(query)
	print "update"
	alpha = .5
	return update_topic_weights(adj_matrix, sen_weights, alpha)
	 


############TEST STUFF################

def test_update_weights(doc):
	sens = clean_document_and_return_sentances(doc)
	print sens
	adj_matrix = create_sentence_adj_matrix(sens)
	print adj_matrix
	adj_matrix = update_graph_with_query(adj_matrix, "wolf")
	print adj_matrix




def test_search(doc):
	fwd = metapy.index.make_forward_index('config.toml')
	rocchio = metapy.index.Rocchio(fwd)

	sens = clean_document_and_return_sentances(doc)
	#print [(str(i) + " : " + sens[i]) for i in xrange(len(sens))]
	results = get_scores_for_doc("wolf")
	print results
	return results

#	sens = clean_document_and_return_sentances("Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 1 of 10IN THE UNITED STATES DISTRICT COURT FOR THE DISTRICT OF COLORADO Civil Action No. 1:15-cv-00270 GEORGE BACA, Plaintiff, v. PARKVIEW MEDICAL CENTER,  INC., and PARKVIEW HEALTH SYSTEMS, INC.,  Defendants. COMPLAINT Plaintiff George Baca, by and through his attorneys, the Civil Rights Education and Enforcement Center, hereby brings this Complaint against Parkview Medical Center, Inc. and Parkview Health Systems, Inc. collectively, Parkview.  INTRODUCTION 1.Twenty-four years after the Americans with Disabilities Act ADA was passedand more than 40 years after Section 504 of the Rehabilitation Act Section 504, Parkview failed to provide sign language interpreters and other accommodations for the deaf father of a critically injured minor, denying him effective communication and deeply exacerbating an already stressful situation.  Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 2 of 10JURISDICTION AND VENUE 2. This action arises under the laws of the United States.  Jurisdiction is conferred upon this court pursuant to 28 U.S.C.  1331 and 1343 for the federal law claims, and 28 U.S.C.  1367 for the state law claim.  3. Venue is proper in this Court pursuant to 28 U.S.C.  1391b2, as all of the events giving rise to the claims occurred in the District of Colorado.  PARTIES 4. Plaintiff George Baca is currently and at all times relevant to this suit has been a resident of the State of Colorado in Pueblo County.  Mr. Baca is an individual with a disability because he is substantially limited in major life activities, including hearing.  5. Defendants Parkview Medical Center, Inc. and Parkview Health Systems, Inc. are private, nonprofit corporations one or both of which own, operate, lease and/or lease to a private hospital, the Parkview Medical Center, which is a place of public accommodation as that term is used in title III of the Americans with Disabilities Act, 42 U.S.C.  121817  and the Colorado Anti-Discrimination Act, COLO. REV. STAT. 24-34-601.  On information and belief, both Parkview Defendants are recipients of federal financial assistance as that term is used in Section 504.  On information and belief, Parkview Medical Center employs more than 15 people.   FACTUAL ALLEGATIONS 6. Plaintiff Baca is deaf, and does not understand speech.  His first language and primary mode of communication is American Sign Language.  7. Like many individuals who have been deaf since childhood, Mr. Baca does not read or write with fluency.  American Sign Language, not English, is his native language.  2 Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 3 of 108. In order to communicate effectively with strangers and/or in situations that call for more than routine language, Mr. Baca requires the services of a qualified sign language interpreter.  Specifically, he requires a sign language interpreter in communications relating to medical topics and in conversations involving multiple individuals.  9. 10. At all times relevant to this lawsuit, Parkview has known that Mr. Baca is Deaf.  On the evening of July 6, 2013, Mr. Baca was notified that his minor daughter was struck by a car and taken by ambulance to Parkview.  He arrived at the hospital not long after.   11. In the emergency room lobby, Mr. Baca immediately requested to see his daughter and to be provided a sign language interpreter.  No interpreter was provided.    12. On the evening of July 6, for most of July 7, and for the morning of July 8, Mr. Baca repeatedly requested an interpreter to speak with doctors, nurses, and other hospital staff.  He was receiving no effective communication concerning what staff were doing and desperately wanted to understand.   13.  Mr. Baca requested a sign language interpreter on July 6, 2013.  14. Defendants did not provide an interpreter for Mr. Baca on July 6, 2013.   15.  Mr. Baca requested a sign language interpreter on the morning of July 7, 2013.    16. Defendants did not provide an interpreter for Mr. Baca until approximately noon on July 7, 2013.  17. The interpreter Defendants provided to Mr. Baca on July 7, 2013 interpreted for him for approximately two hours.    3 Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 4 of 1018. After the interpreter provided to Mr. Baca on July 7, 2013 left, Defendants did not provide an interpreter for Mr. Baca for the remainder of that day.    19. On the morning of July 8, 2013, medical staff met in Mr. Bacas daughters hospital room to discuss her condition.   20.  Mr. Baca again requested an interpreter for this meeting.   21. Parkview did not provide an interpreter for the meeting with medical personnel on the morning of July 8, 2013.   22. Although a sign language interpreter was provided later in the day on July 8, medical personnel did not return to Mr. Bacas daughters room to discuss her condition in the presence of the interpreter.  23.  When Mr. Baca arrived at the Emergency Room on the evening of July 6, he was unable to understand what Parkview staff were telling him about his daughters condition.  The only way the doctor could convey the extent of Mr. Bacas daughters injuries was to pull back the curtain on her room and show Mr. Baca her critical injuries. Without effective communication to convey the context of his daughters injuries, this was terrifying for him. 24.  Mr. Baca was asked to sign documents pertaining to his daughters care.   25.  Mr. Baca did not fully understand the documents he was requested to sign because Defendants did not provide a sign language interpreter to assist him.   26. Parkview was on notice that Mr. Baca needed an interpreter both because the need was obvious, and because on a number of occasions during his daughters stay, Mr. Baca requested an interpreter.   4 Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 5 of 1027. On two occasions, a nurse attempted to communicate with Mr. Baca in writing about his daughters care, the result of which were notes saying, She doesnt need surgery, and The doctor said he can come back. He is saying he sic injury is something that will heel sic on its own.  We will do a CAT scan in the morning to Double Check. In response to the former, Mr. Baca wrote  to underscore his need for an interpreter  dont matter I must I know everything Because I will take care her when out hospital. In response to the latter, he wrote, OK for now Interpreter 24/7!!!!   28. Parkview either lacks policies and procedures sufficient to ensure timely provision of effective communication or has policies and procedures that are inadequate to ensure this. 29. Parkview denied Mr. Baca access to communication as effective as that available to hearing parents of patients in its health care facilities.  30. The actions above discriminated against Mr. Baca on the basis of his disability. 31.  Mr. Baca was harmed by Parkviews discrimination and failure to make its aids, benefits, and services available to him on nondiscriminatory terms.  The discrimination and absence of effective communication, themselves, harmed Mr. Baca.  In addition, he suffered emotional harm from the experience of coping with his daughters critical injuries without the communication and information essential to any parent in that situation.  Throughout the first three days of his daughters hospitalization for life-threatening injuries, he felt intensely emotional, helpless, and frustrated.   32.  Mr. Baca and his family members have received services at Parkview on multiple occasions and Mr. Baca intends to continue to use Parkview as the principal hospital for himself  5 Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 6 of 10and his family for emergency or inpatient care.  Parkview is the only Level II Medical Center in the region where he resides. For these reasons, it is likely that Mr. Baca will in the future be a patient or the companion of a patient receiving medical care at Parkview and, in the absence of the relief requested in this Complaint, likely encounter further illegal discrimination.   FIRST CLAIM FOR RELIEF Violations of Section 504 of the Rehabilitation Act 33. Plaintiff incorporates the allegations set forth in the remainder of this Complaint and in each of the above paragraphs as if fully set forth herein.  34. Section 504 prohibits discrimination on the basis of disability by recipients of federal financial assistance such as Parkview.  28 U.S.C. 794.  35.  Mr. Baca is an individual with a disability within the meaning of the Section 504.  36. Parkview discriminated against Mr. Baca on the basis of disability in violation of Section 504 and its implementing regulations as more fully described above. Such discrimination includes but is not limited to the failure to provide auxiliary aids and services necessary to ensure effective communication and failure to provide aids, benefits and services as effective as those provided to others. 37.  Mr. Baca was qualified to participate in Defendants aids, benefits, and services within the meaning of Section 504.  38. Defendants denied Mr. Baca access to their aids, benefits, and services solely on the basis of his disability, thereby violating Section 504.  39. Despite the clear provisions of Section 504, Defendants knowledge of Mr. Bacas requests for an interpreter, and its knowledge of Mr. Bacas deafness and need for  6 Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 7 of 10accommodation, Defendants continued to impose conditions and practices that discriminated against Mr. Baca.  40. Defendants actions described in this Complaint were intentional and/or were taken with deliberate indifference to the strong likelihood that pursuit of its questioned policies would likely result in a violation of Mr. Bacas rights under the ADA and Section 504.   41. As a direct and proximate result of the acts, omissions, and violations alleged above, Mr. Baca has suffered damages, including but not limited to pain and suffering, inconvenience, and emotional distress.  42.  Mr. Baca has been injured and aggrieved by and will continue to be injured and aggrieved by Defendants discrimination.   SECOND CLAIM FOR RELIEF Violations of title III of the Americans with Disabilities Act. 43. Plaintiff incorporates the allegations set forth in each of the above paragraphs and  remainder of this Complaint as if fully set forth herein.  44. Title III of the ADA prohibits discrimination on the basis of disability by entities such as Defendants who own, operate, lease or lease to places of public accommodation.  42 U.S.C.  12182 et seq.  45. Parkview Medical Center is a place of public accommodation as that term is used in title III of the ADA.  42 U.S.C.  121817F.  46.  Mr. Baca is an individual with a disability within the meaning of the ADA.  47. Defendants discriminated against Mr. Baca on the basis of disability in violation of title III of the ADA and its implementing regulations as more fully described above.  Such  7 Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 8 of 10discrimination includes but is not limited to the failure to provide auxiliary aids and services and the failure to provide communication equally effective to that provided to others. 48.  Mr. Baca was qualified to participate in Defendants goods, services, facilities, privileges, advantages, and accommodations within the meaning of title III of the ADA. 49. Defendants denied Mr. Baca services, and otherwise treated him differently on the basis of his disability, thereby violating title III of the ADA. 50. Despite the clear provisions of title III, Defendants knowledge of Mr. Bacas requests for an interpreter, and its knowledge of Mr. Bacas deafness and need for accommodation, Defendants continued to impose conditions and practices that discriminated against Mr. Baca.  51. As a direct and proximate result of the acts, omissions, and violations alleged above, Mr. Baca has suffered damages including but not limited to pain and suffering, inconvenience, emotional distress, and impairment of quality of life.  52.  Mr. Baca has been injured and aggrieved by and will continue to be injured and aggrieved by Defendants discrimination.  THIRD CLAIM FOR RELIEF Violations of the Colorado Anti-Discrimination Act. 53. Plaintiff incorporates the allegations set forth in each of the above paragraphs of this Complaint as if fully set forth herein.  54. Parkview is a place of public accommodation as defined in C.R.S.  24-34-6011. 55. C.R.S.  24-34-6012 provides in relevant part that it is a discriminatory practice and unlawful for a person, directly or indirectly, to refuse, withhold from, or deny to an  8 Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 9 of 10individual or a group, because of disability . . . the full and equal enjoyment of the goods, services, facilities, privileges, advantages, or accommodations of a place of public accommodation . . . 56. By, among other things, failing to provide effective communication services to Mr. Baca on July 6, 7, 8 and at other times while his daughter was receiving services at Parkview, despite their knowledge that he was Deaf, and despite his repeated requests for interpreter services, Defendants discriminated against Mr. Baca by denying him the full and equal enjoyment of the goods, services, facilities, privileges, advantages, or accommodations of the Center in violation of C.R.S.  24-34-601.   WHEREFORE, Plaintiff respectfully requests: 1. 2. That this Court assume jurisdiction;  That this Court declare the actions of Defendants described in this Complaint to be in violation of title III of the Americans with Disabilities Act, Section 504, and the Colorado Anti-Discrimination Act; 3. That this Court enter an injunction ordering Defendants to cease discrimination on the basis of disability against deaf patients and companions of patients, including but not limited to Mr. Baca, by among other things establishing a procedure to ensure effective communication with persons who are deaf or hard of hearing; 4. That this Court award Mr. Baca compensatory damages pursuant to Section 504 and the Colorado Anti-Discrimination Act;  5. That this Court award Mr. Baca and/or his attorneys his reasonable attorneys fees and costs; and  9 Case 1:15-cv-00270-RBJ   Document 1   Filed 02/09/15   USDC Colorado   Page 10 of 106. That this Court award such additional or alternative relief as may be just, proper, and equitable.   Dated this 9th day of February, 2015.  Respectfully submitted,  s/ Amy F. Robertson ___________________________________ Amy F. Robertson Civil Rights Education and Enforcement Center 104 Broadway, Suite 400 Denver, CO 80203 Phone: 303 757-7901 arobertson@creeclaw.org   Attorney for Plaintiff  10 ")
#	print [(str(i) + " : " + sens[i]) for i in xrange(len(sens))]
	#idx = metapy.index.make_inverted_index('summarizer/config.toml')
	#num_results = idx.num_docs()
	#print num_results
	# Build the query object and initialize a ranker
	#query = metapy.index.Document()
	#ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)

	#query.content("shortest path")
	#results = ranker.score(idx, query, num_results)

#	results = sorted(results, key = lambda doc: int(doc[0]))
#	results = get_scores_for_doc(rocchio, "certain villag")
#	print results
if __name__ == '__main__':
	if(os.path.exists('idx')):
		shutil.rmtree('idx')
	doc = "Once upon a time there lived in a certain village a little country girl, the prettiest creature who was ever seen. Her mother was excessively fond of her; and her grandmother doted on her still more. This good woman had a little red riding hood made for her. It suited the girl so extremely well that everybody called her Little Red Riding Hood. One day her mother, having made some cakes, said to her, \"Go, my dear, and see how your grandmother is doing, for I hear she has been very ill. Take her a cake, and this little pot of butter.\" Little Red Riding Hood set out immediately to go to her grandmother, who lived in another village. As she was going through the wood, she met with a wolf, who had a very great mind to eat her up, but he dared not, because of some woodcutters working nearby in the forest. He asked her where she was going. The poor child, who did not know that it was dangerous to stay and talk to a wolf, said to him, \"I am going to see my grandmother and carry her a cake and a little pot of butter from my mother.\" \"Does she live far off?\" said the wolf \"Oh I say,\" answered Little Red Riding Hood; \"it is beyond that mill you see there, at the first house in the village.\" \"Well,\" said the wolf, \"and I\'ll go and see her too. I\'ll go this way and go you that, and we shall see who will be there first.\" The wolf ran as fast as he could, taking the shortest path, and the little girl took a roundabout way, entertaining herself by gathering nuts, running after butterflies, and gathering bouquets of little flowers. It was not long before the wolf arrived at the old woman\'s house. He knocked at the door: tap, tap. \"Who\'s there?\" \"Your grandchild, Little Red Riding Hood,\" replied the wolf, counterfeiting her voice; "
	#doc = "The fox dog it. foot grazed the sleeping. The fox waking it."
	#test_search(doc)
	test_update_weights(doc)

