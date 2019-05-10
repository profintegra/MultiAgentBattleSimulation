import numpy as np
import random
from models import TorchEstimator
import torch

class Agent():
    def __init__(self,agentId,max_life,team,identity=0,viewrange=2,attackrange=1,moverange=2):
        self.agentId = agentId
        self.position = None
        self.estimator = TorchEstimator(viewrange,moverange,attackrange)
        self.life = max_life
        self.reward = 0
        self.alive = True
        self.team = team
        self.identity = identity
        self.viewrange = viewrange
        self.attackrange = attackrange
        self.moverange = moverange
        self.damage = 100
        self.create_model()
    #getters
    def getId(self):
        return self.agentId

    def getPosition(self):
        return self.position

    def getEstimator(self):
        return self.estimator

    def getLife(self):
        return self.life

    def getReward(self):
        return self.reward

    def isAlive(self):
        return self.alive

    def getTeam(self):
        return self.team

    def getIdentity(self):
        return self.identity

    def getViewRange(self):
        return self.viewrange

    def getAttackRange(self):
        return self.attackrange

    def getMoveRange(self):
        return self.moverange

    def getDamage(self):
        return self.damage

    #setters
    def setPosition(self,coord):
        self.position = coord

    def setViewRange(self,r):
        self.viewrange = r

    def setAttackRange(self,r):
        self.attackrange = r

    #processers
    def deliverDamage(self,damage,target_agent):
        self.reward += damage
        alive = target_agent.processDamage(damage)
        if alive == False:
            self.reward += 50
        return alive

    def processDamage(self,damage):
        self.life -= damage
        self.reward -= damage
        if self.life <= 0:
            self.alive = False
            self.reward -= 100
        return self.alive

    def update(self,coord,reward):
        self.position = coord
        self.reward += reward

    def create_model(self):
        self.policy = self.random_policy

    def generateActionSpace(self):
        return np.zeros((1 + self.moverange*2)**2 + (1 + self.actionrange*2)**2)

    def train_policy(self,state,actions):
        with torch.no_grad():
            actions = torch.tensor(actions).float()
            state = torch.tensor(state).float()
        probs = self.estimator(state,actions)
        action_probs = probs.clone().detach().numpy().flatten()
        return np.random.choice(action_probs.shape[0],p=action_probs)
        # move_range = (1+self.moverange*2)**2
        # acton_range = (1+self.attackrange*2)**2

        # return self.random_policy(probs.clone().detach().numpy())

    def move(self,action):
        self.position = action

    def random_policy(self,probs):
        return random.choice(len(probs),p=probs)

    def serialize(self):
        return {"agentId":self.agentId,"alive":self.alive,"team":self.team,"life":self.life,
                "position":self.position,"identity":self.identity,
                "viewrange":self.viewrange,"attackrange":self.attackrange,"reward":self.reward}

