import json
from SoleraConnector import SoleraConnector

def query_for_artifacts(start_date,start_time,end_date,end_time,gmtoffset,ip_addr):
        s = SoleraConnector("username","token","hostname")
        z=json.loads(json.dumps(s.callAPI("GET", "/artifacts/artifacts",{'identityPath':'/timespan/'+start_date+'T'+start_time+gmtoffset+'_'+end_date+'T'+end_time+gmtoffset+'/ipv4_address/'+ip_addr})))
        return z

def get_artifact_details(selected_artifact):
        params={
                'artifactIDs':[selected_artifact]
        }
        s = SoleraConnector("username","token","hostname")
        z=json.loads(json.dumps(s.callAPI("GET","/artifacts/details",params),indent=5))

        for artifact in z['result']['artifacts']:
                if artifact['Artifact']['protocol']=="smtp":
                        parse_smtp_results(z)
                else:
                        print json.dumps(z,indent=5)


def export_artifact(selected_artifact):
        #Get the filename
        params={
                'artifactIDs':[selected_artifact]
        }
        s = SoleraConnector("username","token","hostname")
        z=json.loads(json.dumps(s.callAPI("GET","/artifacts/details",params),indent=5))
        for name in z['result']['artifacts']:
                filename=name['Artifact']['filename'].rsplit('/',1)
                filename=filename[-1]
                session_id=name['Artifact']['artifact_search_id']
        print selected_artifact
        print filename
        print session_id
        #Download file
        params={
                'ids':[selected_artifact],
                'searchId':session_id
        }
        s = SoleraConnector("username","token","hostname")
        print(s.callAPI("GET","/artifacts/download",params,filename))

def parse_smtp_results(z):
        import datetime
        for artifact in z['result']['artifacts']:
                print "\r\n"
                print "Title: %s" %artifact['Artifact']['title']
                print "Protocol: %s" %artifact['Artifact']['protocol']
                print "Time: %s" %datetime.datetime.fromtimestamp(artifact['Artifact']['capture_start_time']).strftime('%Y-%m-%d %H:%M:%s')
                if artifact['Artifact']['meta_info']:
                        print "\r\n"
                        print "***** Envelope information ******************"
                        print "Sender: %s" %artifact['Artifact']['meta_info']['email_from']
                        print "Subject: %s" %artifact['Artifact']['meta_info']['email_subject']
                        print "Recipients: %s" %artifact['Artifact']['meta_info']['email_to']
                        print "MessageID: %s" %artifact['Artifact']['meta_info']['email_messageid']
                        print "***************************************"
                        print "\r\n"
                print "Message size: %s" %artifact['Artifact']['filesize']
                print "Message SHA1: %s" %artifact['Artifact']['sha1']
                print "Message MD5: %s" %artifact['Artifact']['md5']
                print "\r\n"
                print "Sender IP: %s" %artifact['Artifact']['source_ip']
                print "Recipient IP: %s" %artifact['Artifact']['destination_ip']
                if artifact['Artifact']['attachments']:
                        for attachment in artifact['Artifact']['attachments']:
                                print "Email has an attachment!"
                                print "Attachment name: %s" %attachment['Artifact']['host']
                                print "Attachment type: %s" %attachment['Artifact']['magic_type']
                                print "Claimed type: %s" %attachment['Artifact']['mime_type']
                                print "File size: %s" %attachment['Artifact']['filesize']
                                print "File SHA1: %s" %attachment['Artifact']['sha1']
                                print "File MD5: %s" %attachment['Artifact']['md5']
                                print "ID: %s" %attachment['Artifact']['id']
