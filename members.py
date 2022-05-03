import json
from dataclasses import dataclass
import qqbot
from qqbot.model.member import Member
from qqbot.model.guild_member import QueryParams

@dataclass
class MemberStat():
    member : Member
    thanked_total: int = 0
    thanked_this_month: int = 0
    thanked_this_week: int = 0
    thanked_today: int = 0
    liked_total: int = 0
    liked_this_month: int = 0
    liked_this_week: int = 0
    liked_today: int = 0

class MemberStatistics:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        try:
            self.members = self.readDb()
            self.updateDb()
        except json.decoder.JSONDecodeError:
            self.members = {}
            self.updateDb()

    def toJSON(self,obj):
        return json.dumps(obj,default=lambda o: o.__dict__,sort_keys=False ,indent=4)

    def readDb(self):
        with open('db.json',"r", encoding="utf-8") as db:
            all_members = json.load(db)
            return all_members
        
    def writeDb(self):
        with open('db.json',"w", encoding="utf-8") as db:
            # db.write(self.membersToJSON())
            json.dump(self.members, db, sort_keys=False, indent=4)
            # json.dump(json.loads(self.membersToJSON()), db, sort_keys=True, indent=4)

    def updateDb(self):
        guild_member_api = qqbot.GuildMemberAPI(self.token,False)
        guild_member_pager = QueryParams(after="0",limit=1)
        g_members = guild_member_api.get_guild_members(self.guild_id,guild_member_pager) 
        for m in g_members:
            if m.user.id not in self.members:
                self.members[m.user.id] = json.loads(self.toJSON(MemberStat(member = m)))
            else:
                self.members[m.user.id]["member"] = json.loads(self.toJSON(m))
        self.writeDb()

    def clearLeft(self):
        guild_member_api = qqbot.GuildMemberAPI(self.token,False)
        guild_member_pager = QueryParams(after="0",limit=1)
        g_members = guild_member_api.get_guild_members(self.guild_id, guild_member_pager) 
        mids = [m.user.id for m in g_members]
        for m in self.members:
            if m not in mids:
                self.members.pop(m)
        