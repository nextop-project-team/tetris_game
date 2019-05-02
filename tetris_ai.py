#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tetris_model import BOARD_DATA, Shape   #BOARD_DATA, shape 받아옴
import math
from datetime import datetime
import numpy as np
#블럭모양
 #ㅁㅁ     ㅁㅁ  ㅁㅁㅁ    ㅁㅁ
  # ㅁㅁ   ㅁㅁ    ㅁ    ㅁㅁ
  #    Z모양  O모양  T모양  S모양
   #ㅁ                 
   #ㅁ     ㅁ        ㅁ
   #ㅁ     ㅁ        ㅁ
   #ㅁ     ㅁㅁ    ㅁㅁ
  #I모양   L모양   J모양


class TetrisAI(object):

    def nextMove(self): #다음 움직임
        t1 = datetime.now() #t1 = 현재시간
        if BOARD_DATA.currentShape == Shape.shapeNone: #model의 현재모양이 없으면 None
            return None

        currentDirection = BOARD_DATA.currentDirection #model에서 현재 방향 받아옴
        currentY = BOARD_DATA.currentY #model 에서 현재 Y 받아옴
        _, _, minY, _ = BOARD_DATA.nextShape.getBoundingOffsets(0) #최소 Y값 받아옴
        nextY = -minY #다음Y = -최소Y

        # print("=======")
        strategy = None  #전략? None
        if BOARD_DATA.currentShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS): #현재블럭모양 I,Z,S이면
            d0Range = (0, 1)
        elif BOARD_DATA.currentShape.shape == Shape.shapeO: #현재블럭모양 O이면
            d0Range = (0,)
        else:#나머지(T,L,J)
            d0Range = (0, 1, 2, 3)

        if BOARD_DATA.nextShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS): #다음블럭모양 I,Z,S이면
            d1Range = (0, 1)
        elif BOARD_DATA.nextShape.shape == Shape.shapeO: #다음블럭모양 O이면
            d1Range = (0,)
        else: #나머지(T,L,J)
            d1Range = (0, 1, 2, 3)

        for d0 in d0Range: #위에서 설정한 d0 범위 탐색
            minX, maxX, _, _ = BOARD_DATA.currentShape.getBoundingOffsets(d0) #최소,최대X설정
            for x0 in range(-minX, BOARD_DATA.width - maxX): # 범위 -최소x,보드너비-최대x
                board = self.calcStep1Board(d0, x0)
                for d1 in d1Range: #d1범위 탐색
                    minX, maxX, _, _ = BOARD_DATA.nextShape.getBoundingOffsets(d1)
                    dropDist = self.calcNextDropDist(board, d1, range(-minX, BOARD_DATA.width - maxX)) #떨어지는거리?
                    for x1 in range(-minX, BOARD_DATA.width - maxX): #범위(-최소x,보드너비-최대x)
                        score = self.calculateScore(np.copy(board), d1, x1, dropDist)
                        if not strategy or strategy[2] < score: #strategy또는 strategy[2]둘중하나라도 < score 면
                            strategy = (d0, x0, score) #strategy = 현재값
        print("===", datetime.now() - t1)
        print(strategy)
        return strategy

    def calcNextDropDist(self, data, d0, xRange):
        res = {} #res배열생성
        for x0 in xRange:#xRange는 range와 비슷,데이터 타입차이
            if x0 not in res:
                res[x0] = BOARD_DATA.height - 1 #res[x0]= 보드높이-1
            for x, y in BOARD_DATA.nextShape.getCoords(d0, x0, 0): #다음블럭좌표값
                yy = 0
                while yy + y < BOARD_DATA.height and (yy + y < 0 or data[(y + yy), x] == Shape.shapeNone):
                    yy += 1
                yy -= 1
                if yy < res[x0]:
                    res[x0] = yy
        return res

    def calcStep1Board(self, d0, x0):
        board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width)) #board = 배열(getData)생성 후, BOARD_DATA의 높이와 너비를 받아와 배열 정리
        self.dropDown(board, BOARD_DATA.currentShape, d0, x0)
        return board

    def dropDown(self, data, shape, direction, x0): #블록모양, 방향
        dy = BOARD_DATA.height - 1 #dy = 보드높이 -1
        for x, y in shape.getCoords(direction, x0, 0): # 블록 방향만큼 돌림
            yy = 0 #yy 0으로 설정
            while yy + y < BOARD_DATA.height and (yy + y < 0 or data[(y + yy), x] == Shape.shapeNone):
                yy += 1 #yy + y 가 보드 높이보다 작고, [ yy + y 가 0보다 작거나 블록이 없을동안] yy에 1을 더함
            yy -= 1
            if yy < dy: #yy가 dy(보드높이-1)보다 작을경우
                dy = yy
        # print("dropDown: shape {0}, direction {1}, x0 {2}, dy {3}".format(shape.shape, direction, x0, dy))
        self.dropDownByDist(data, shape, direction, x0, dy)

    def dropDownByDist(self, data, shape, direction, x0, dist):
        for x, y in shape.getCoords(direction, x0, 0):
            data[y + dist, x] = shape.shape

    def calculateScore(self, step1Board, d1, x1, dropDist): #점수계산
        # print("calculateScore")
        t1 = datetime.now() #현재시간
        width = BOARD_DATA.width #보드 너비높이지정
        height = BOARD_DATA.height

        self.dropDownByDist(step1Board, BOARD_DATA.nextShape, d1, x1, dropDist[x1])
        # print(datetime.now() - t1)

        # Term 1: lines to be removed
        fullLines, nearFullLines = 0, 0
        roofY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width
        vHoles, vBlocks = 0, 0
        for y in range(height - 1, -1, -1):
            hasHole = False  #라인에 블럭유무확인
            hasBlock = False
            for x in range(width):
                if step1Board[y, x] == Shape.shapeNone: #블럭없으면 hashole = True
                    hasHole = True
                    holeCandidates[x] += 1
                else:
                    hasBlock = True #블럭있으면 hasblock = True
                    roofY[x] = height - y
                    if holeCandidates[x] > 0:
                        holeConfirm[x] += holeCandidates[x]
                        holeCandidates[x] = 0
                    if holeConfirm[x] > 0:
                        vBlocks += 1
            if not hasBlock:
                break
            if not hasHole and hasBlock:
                fullLines += 1
        vHoles = sum([x ** .7 for x in holeConfirm])
        maxHeight = max(roofY) - fullLines
        # print(datetime.now() - t1)

        roofDy = [roofY[i] - roofY[i+1] for i in range(len(roofY) - 1)]

        if len(roofY) <= 0:
            stdY = 0
        else:
            stdY = math.sqrt(sum([y ** 2 for y in roofY]) / len(roofY) - (sum(roofY) / len(roofY)) ** 2)
        if len(roofDy) <= 0:
            stdDY = 0
        else:
            stdDY = math.sqrt(sum([y ** 2 for y in roofDy]) / len(roofDy) - (sum(roofDy) / len(roofDy)) ** 2)

        absDy = sum([abs(x) for x in roofDy]) #absDy += x의 절댓값
        maxDy = max(roofY) - min(roofY)
        (datetime.now() - t1)

        score = fullLines * 1.8 - vHoles * 1.0 - vBlocks * 0.5 - maxHeight ** 1.5 * 0.02 \
            - stdY * 0.0 - stdDY * 0.01 - absDy * 0.2 - maxDy * 0.3
       # print(score, fullLines, vHoles, vBlocks, maxHeight, stdY, stdDY, absDy, roofY, d0, x0, d1, x1)
        return score


TETRIS_AI = TetrisAI()

