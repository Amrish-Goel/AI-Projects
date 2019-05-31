import time

start = time.time()

def time_check():
    time_period = 177
    if time.time() > start + time_period:
        return True
    return False

def write(printValue):
    write = open('output.txt', 'w')
    write.write(printValue)
    write.close()

def evaluate_space(g_counter,req):
   temp=[]*7
   count, flag=0, 0
   for i in req:
       temp.append(g_counter[count] - int(i))
       if temp[count]==-1:
           flag=1;
           break;
       count+=1

   if (flag == 1):
       return -1
   else:
       g_counter[:]=list(temp)
       return 0

def return_max(sort_list):
    n = int(sort_list[1])
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r

class Greedy:
    spla_counter = []
    lahsa_counter = []

    def __init__(self, bothSL, onlyS, onlyL, bed_list, park_list):
        self.bothSL = bothSL
        self.onlyS = onlyS
        self.onlyL = onlyL
        self.spla_list = self.create_list(onlyS)
        self.lahsa_list = self.create_list(onlyL)
        self.spla_lahsa_list = self.create_list(bothSL)
        self.spla_counter = park_list
        self.lahsa_counter = bed_list


    def create_list(self,list):
        result =[]
        for candidate in list:
            result.append([candidate.getId(), candidate.days])
        return result




    def greed(self,spla_list,lahsa_list,spla_lahsa_list):
        # sort the eligibility lists by requested number of days
        spla_list.sort(key=return_max, reverse=True)
        lahsa_list.sort(key=return_max, reverse=True)
        spla_lahsa_list.sort(key=return_max, reverse=True)

        # initialize the chosen applicants lists
        spla_chosen_appl = []
        lahsa_chosen_appl = []
        applicable = 1
        for i in range(len(spla_lahsa_list)):
            if (i % 2 == 0):
                if evaluate_space(self.spla_counter, str(spla_lahsa_list[i][1])) != -1:
                    spla_chosen_appl.append(spla_lahsa_list[i][0])
                else:
                    applicable = 0
                    break
            else:
                if (evaluate_space(self.lahsa_counter, str(spla_lahsa_list[i][1])) != -1):
                    lahsa_chosen_appl.append(spla_lahsa_list[i][0])
                else:
                    applicable = 0
                    break


        if applicable:

            for i in range(len(spla_list)):
                if evaluate_space(self.spla_counter, str(spla_list[i][1])) != -1:
                    spla_chosen_appl.append(spla_list[i][0])
                else:
                    applicable = 0
                    break

        if applicable:
            for i in range(len(lahsa_list)):
                if (evaluate_space(self.lahsa_counter, str(lahsa_list[i][1])) != -1):
                    spla_chosen_appl.append(lahsa_list[i][0])
                else:
                    #print("Warning: Applicants left but space empty")
                    applicable = 0
                    break

        if not spla_lahsa_list and not spla_list:
            return "00000"
        elif not spla_lahsa_list:
            return spla_list[0][0]
        else:
            return spla_lahsa_list[0][0]




class Candidate:
    def __init__(self, id, gender, age, pets, medical, car, license, days):
        self.id = id
        self.gender = gender
        self.age = age
        if pets =='Y':
            self.pets = True
        else:
            self.pets = False

        if medical == 'Y':
            self.medical = True
        else:
            self.medical = False

        if car == 'Y':
            self.car = True
        else:
            self.car = False

        if license == 'Y':
            self.license = True
        else:
            self.license = False

        self.days = days
        self.type = self.classify()
        self.resources = self.getResourcesCount()

    def classify(self):
        if self.car and self.license and not self.medical and self.age > 17 and self.gender == 'F' and not self.pets:
            return 'BP'
        if self.car and self.license and not self.medical:
            return 'SP'
        if not (not (self.age > 17) or not (self.gender == 'F') or self.pets):
            return 'LP'
        return 'N'

    def getResourcesCount(self):
        sum = 0
        for i in self.days:
            sum += int(i)
        return sum

    def getDaysAsList(self):
        result = []
        for i in self.days:
            result.append(int(i))
        return result

    def getIntGender(self):
        if self.gender=='F':
            return 1
        return 0

    def setType(self,type):
        self.type = type

    def getId(self):
        return self.id


class Resource:
    def __init__(self, b, p):
        self.b = b
        self.p = p
        self.bedList = [b, b, b, b, b, b, b]
        self.parkList = [p, p, p, p, p, p, p]


    def removeLAHSAFinal(self, list):
        for i in range(7):
            self.bedList[i]=self.bedList[i]-list[i]

    def removeSPLAFinal(self, list):
        for i in range(7):
            self.parkList[i] = self.parkList[i]-list[i]

    def isValidList(self, list):
        for i in range(7):
            if list[i] < 0:
                return False
        return True

    def removeProbable(self, list, type):
        res = []
        if type == "SPLA":
            for i in range(7):
                res.append(self.parkList[i] - list[i])
        else:
            if type == "LAHSA":
                for i in range(7):
                    res.append(self.bedList[i] - list[i])
        return res

    def add_resource(self,candidate, type):
        if(type=="SPLA"):
            list = candidate.getDaysAsList();
            for i in range(7):
                self.parkList[i]=self.parkList[i]+list[i]
            return self.parkList
        if (type == "LAHSA"):
            list = candidate.getDaysAsList();
            for i in range(7):
                self.bedList[i] = self.bedList[i] + list[i]
            return self.bedList

    def sum(self, type):
        sum = 0
        if (type == "LAHSA"):
            for i in range(7):
                sum = sum + int(self.bedList[i])
        else:
            for i in range(7):
                sum = sum + int(self.parkList[i])
        return sum

    def greater(self, resource, type):
        sumSelf = self.sum(type)
        sumResource = resource.sum(type)

        if(sumSelf > sumResource):
            return "true"
        if(sumSelf < sumResource):
            return "false"
        if(sumSelf==sumResource):
            return "equal"

def populateType(list, candidate_type, candidate_list):
    for x in range(len(list)):
        candidate_list[int(list[x])-1].setType(candidate_type)

def extract_candidate_input(data):
    id = data[0:5]
    gender = data[5]
    age = int(data[6:9])
    pets = data[9]
    medical = data[10]
    car = data[11]
    license = data[12]
    days = data[13:20]
    return id, gender, age, pets, medical, car, license, days

def parse_input():
    with open('input1.txt') as read:
        b = int(read.readline())
        p = int(read.readline())

        no_lahsa_candidates_already_chosen = int(read.readline())
        lahsa_list = []
        for i in range(no_lahsa_candidates_already_chosen):
            lahsa_list.append(str(read.readline()))

        no_spla_candidates_already_chosen = int(read.readline())
        spla_list = []
        for i in range(no_spla_candidates_already_chosen):
            spla_list.append(str(read.readline()))

        total_candidates = int(read.readline())
        check = False
        if total_candidates <= p:
            check = True
        candidate_list = []
        for i in range(total_candidates):
            id, gender, age, pets, medical, car, license, days = extract_candidate_input(read.readline())
            candidate = Candidate(id, gender, age, pets, medical, car, license, days)
            candidate_list.append(candidate)

        return b, p, lahsa_list, spla_list, candidate_list, check

def getProbableCandidates(candidate_list, param):
    probable_candidates = []
    for candidate in candidate_list:
        if candidate.type == param:
            probable_candidates.append(candidate)
    return probable_candidates


def isValid(resource_type, resource, candidate, candidate_type):
    check = resource_type.isValidList(resource.removeProbable(resource_type.add_resource(candidate, candidate_type), candidate_type))
    if check == False:
        resource_type.bedList = resource_type.removeProbable(candidate.getDaysAsList(), candidate_type)
        return check
    else:
        return check



def retValue(rC, rCount, type):
    if(type=="SPLA"):
        if(rCount.p==0):
            rCount.p = rC.p
            rCount.b = rC.b
        if(rC.p>rCount.p):
            rCount.p = rC.p
            rCount.b = rC.b
    else:
        if(rCount.b==0):
            rCount.b = rC.b
            rCount.p = rC.p
        if(rC.b>rCount.b):
            rCount.b = rC.b
            rCount.p = rC.p

def getAllValidateCan(fullList, lis):
    return [x for x in fullList if x not in lis]


def lahsaDFS(lahsa_resource, spla_resource, l, lahsa_probable_list, resource, candidate_list, maxRes, rCount):
    if time_check():
        return
    if(len(lahsa_probable_list)==l):
        if(rCount.b<lahsa_resource.sum("LAHSA")):
            rCount.p = spla_resource.sum("SPLA")
            rCount.b = lahsa_resource.sum("LAHSA")

        r = lahsa_resource.greater(maxRes, "LAHSA")
        if r == "equal" or r == "true":
            for i in range(7):
                maxRes.bedList[i] = lahsa_resource.bedList[i]
        return

    for i in range(l,len(lahsa_probable_list)):
        if isValid(lahsa_resource, resource, lahsa_probable_list[i], "LAHSA"):
            lahsaDFS(lahsa_resource, spla_resource, i+1, lahsa_probable_list, resource, candidate_list, maxRes, rCount)
            lahsa_resource.bedList = lahsa_resource.removeProbable(lahsa_probable_list[i].getDaysAsList(), "LAHSA")




def splaDFS(lahsa_resource, spla_resource, s, spla_probable_list, resource, candidate_list, maxRes, rCount):
    if time_check():
        return
    if(len(spla_probable_list)== s):
        if(rCount.p <spla_resource.sum("SPLA")):
            rCount.p = spla_resource.sum("SPLA")
            rCount.b = lahsa_resource.sum("LAHSA")

        r = spla_resource.greater(maxRes, "SPLA")
        if r == "equal" or r == "true":
            for i in range(7):
                maxRes.parkList[i] = spla_resource.parkList[i]
        return

    for i in range(s,len(spla_probable_list)):
        if (isValid(spla_resource, resource, spla_probable_list[i], "SPLA")):
            splaDFS(lahsa_resource, spla_resource, i+1, spla_probable_list,resource, candidate_list, maxRes, rCount)
            spla_resource.parkList = spla_resource.removeProbable(spla_probable_list[i].getDaysAsList(), "SPLA")





def dfsboth(spla_resource, lahsa_resource, s, l, spla_probable_list, lahsa_probable_list, resource, candidate_list, maxRes, sList,lList, turn, rCount):
    if time_check():
        return
    # SPLA turn
    if turn:
        result = getAllValidateCan(getAllValidateCan(spla_probable_list, lList), sList)
        check = True
        for i in range(len(result)):
            if isValid(spla_resource, resource, result[i], "SPLA"):
                check = not check
                sList.append(result[i])
                rC = Resource(0, 0)
                dfsboth(spla_resource, lahsa_resource, s, l, spla_probable_list, lahsa_probable_list, resource, candidate_list, maxRes, sList, lList, not turn, rC)
                retValue(rC, rCount, "SPLA")
                sList.remove(result[i])
                spla_resource.parkList = spla_resource.removeProbable(result[i].getDaysAsList(), "SPLA")

        if check:
            lahsaDFS(lahsa_resource, spla_resource, 0, getAllValidateCan(getAllValidateCan(lahsa_probable_list, lList), sList), resource, candidate_list, maxRes, rCount)
        return

    # LAHSA turn
    if not turn:
        result = getAllValidateCan(getAllValidateCan(lahsa_probable_list, sList), lList)
        check = True
        for i in range(len(result)):
            if isValid(lahsa_resource, resource, result[i], "LAHSA"):
                check = False
                lList.append(result[i])
                rC = Resource(0, 0)
                dfsboth(spla_resource, lahsa_resource, s, l, spla_probable_list, lahsa_probable_list, resource, candidate_list, maxRes, sList, lList, not turn, rC)
                retValue(rC, rCount, "LAHSA")
                lList.remove(result[i])
                lahsa_resource.bedList = lahsa_resource.removeProbable(result[i].getDaysAsList(), "LAHSA")
        if check:
            splaDFS(lahsa_resource, spla_resource, 0, getAllValidateCan(getAllValidateCan(spla_probable_list, sList), lList), resource, candidate_list, maxRes, rCount)
        return


def process(resource, candidate_list, check):
    probable_candidates_both = getProbableCandidates(candidate_list, "BP")
    spla_only_probable_list = getProbableCandidates(candidate_list, "SP")
    lahsa_only_probable_list = getProbableCandidates(candidate_list, "LP")
#     Sorting on both gender and resources
    probable_candidates_both = sorted(probable_candidates_both,key=lambda candidate: (candidate.getIntGender, candidate.resources), reverse= True)
    spla_only_probable_list = sorted(spla_only_probable_list,key=lambda candidate: candidate.resources, reverse=True)
    lahsa_only_probable_list = sorted(lahsa_only_probable_list,key=lambda candidate: candidate.resources, reverse=True)

    greedy = Greedy(probable_candidates_both, spla_only_probable_list, lahsa_only_probable_list, list(resource.bedList), list(resource.parkList))
    greedyAns = greedy.greed(greedy.spla_list, greedy.lahsa_list, greedy.spla_lahsa_list)



    spla_probable_list = probable_candidates_both + spla_only_probable_list
    lahsa_probable_list = probable_candidates_both + lahsa_only_probable_list
    spla_probable_list = sorted(spla_probable_list, key=lambda candidate: candidate.resources, reverse=True)
    lahsa_probable_list = sorted(lahsa_probable_list, key=lambda candidate: candidate.resources, reverse=True)
    id, gender, age, pets, medical, car, license, days = extract_candidate_input(str(greedyAns) + "O000YYNN0000000")
    max_candidate = Candidate(id, gender, age, pets, medical, car, license, days)

    max_resource = Resource(0, 0)
    # iterating taking each spla probable candidate as first choice
    for i in range(len(spla_probable_list)):
        spla_resource = Resource(0, 0)
        lahsa_resource = Resource(0, 0)
        if isValid(spla_resource, resource, spla_probable_list[i], "SPLA"):
            res = Resource(0, 0)
            rCount = Resource(0, 0)
            sList = []
            lList = []
            sList.append(spla_probable_list[i])
            turn = False
            dfsboth(spla_resource, lahsa_resource, i + 1, 0, spla_probable_list, lahsa_probable_list, resource, candidate_list, res, sList, lList, turn, rCount)


            if rCount.p == max_resource.p:
                if rCount.b == max_resource.b:
                    if max_candidate.resources == spla_probable_list[i].resources:
                        if (int(max_candidate.getId()) > int(spla_probable_list[i].getId())):
                            max_candidate = spla_probable_list[i]

                    if max_candidate.resources < spla_probable_list[i].resources:
                        max_candidate = spla_probable_list[i]
                if rCount.b > max_resource.b:
                    max_candidate = spla_probable_list[i]
                    max_resource.b = rCount.b
                if rCount.p > max_resource.p:
                    max_candidate = spla_probable_list[i]
                    max_resource.p = rCount.p
                    max_resource.b = rCount.b
                spla_resource.parkList = spla_resource.removeProbable(spla_probable_list[i].getDaysAsList(), "SPLA")
            if time_check():
                return max_candidate
            return max_candidate


if __name__ == '__main__':
    b, p, lahsa_list, spla_list, candidate_list, check = parse_input()  # type: (int, int, List[str], List[str], List[Candidate])
    write = open('output.txt', 'w')
    output = ""
    resource = Resource(b, p)

    #   populate type to L for LAHSA and S for SPLA if they are already chosen
    #   LP for LAHSA probables and SP for SPLA probables and P for both probables

    populateType(lahsa_list, 'L', candidate_list)
    populateType(spla_list, 'S', candidate_list)

    #   removing resources for whatever is already chosen
    for i in spla_list:
        resource.removeSPLAFinal(candidate_list[int(i) - 1].getDaysAsList())

    for i in lahsa_list:
        resource.removeLAHSAFinal(candidate_list[int(i) - 1].getDaysAsList())

    output = process(resource, candidate_list, check).getId()
    write.write(output)
    write.close()
