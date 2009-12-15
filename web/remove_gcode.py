import sys

if __name__ == "__main__":

    filename = sys.argv[1]
    f = open(filename)
    ll = f.readlines()
    f.close()

    new_ll = []
    skip = False

    print '\ndef get_html (gcode_json):\n    s1 = """\n'

    for i in range(len(ll)):
        l = ll[i]
        if l.find("$$hugomatic$$") > -1:
            skip = False
            # print "NOT SKIPPING",i
            
            
        else:
            if l.find("$hugomatic$") > -1:
                skip = True
                # print "SKIPPING", i
                print "    // $hugomatic$"
                print '"""\n\n    s2 = """\n'    

        if not skip:
            pass        
            print l[0:-1]        
            new_ll.append(l)


    print '"""\n    return s1+gcode_json+s2 \n'

