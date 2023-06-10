import os

import googlemaps

from project.decision_tree.interfaces import IDecisionUseCase
from project.decision_tree.usecase import DecisionTreeUseCaseFactory
from project.entities.decision_tree_node import DecisionTreeNode
from project.entities.place import Place
from project.entities.user import User
from project.entities.user_state import UserState
from project.user.interfaces import IUserUseCase, IUserRepository, IUserStateUseCase, IUserStateRepository
from project.user.repos import UserRepoFactory, UserStateRepoFactory
from project.user.requests import ReceiveMassageRequest, UpdateUserStateRequest
from project.user.response import ReceiveMassageResponse, Status, InitUserStateResponse, InitUserResponse, \
    UpdateUserStateResponse, GetUserStateResponse
from project.entities.user_state import Module
from django.utils.translation import gettext as _

class UserUseCaseFactory(object):
    @staticmethod
    def get() -> IUserUseCase:
        return UserUseCase(UserRepoFactory.get(), DecisionTreeUseCaseFactory.get(), UserStateUseCaseFactory.get())

class UserUseCase(IUserUseCase):
    def __init__(self, repo: IUserRepository, decision_tree_use_case: IDecisionUseCase, user_state_use_case: IUserStateUseCase):
        self.repo = repo
        self.decision_tree_use_case = decision_tree_use_case
        self.user_state_use_case = user_state_use_case

    def set_commands_messages(self, places_message: str, about_message: str, hospital_message: str, pharmacy_message: str):
        self.places_message = places_message
        self.about_message = about_message
        self.hospital_message = hospital_message
        self.pharmacy_message = pharmacy_message

    def init_user(self, chat_id: str) -> InitUserResponse:
        resp = self.repo.get_by_chat_id(chat_id=chat_id)

        if resp is None:
            resp = self.repo.save_user(User(chat_id=chat_id, enabled=True))

        if resp is None:
            return InitUserResponse(status=Status.ERROR)

        if not resp.enabled:
            return InitUserResponse(status=Status.USER_DISABLED)
        status_resp = self.user_state_use_case.init_user_state(resp.id)

        if status_resp.status == Status.ERROR:
            return InitUserResponse(status=Status.ERROR)

        categories = self.decision_tree_use_case.get_categories()

        return InitUserResponse(status=Status.OK, categories=categories)

    def receive_message(self, req: ReceiveMassageRequest) -> ReceiveMassageResponse:
        user = self.repo.get_by_chat_id(chat_id=req.chat_id)

        if user is None:
            user = self.repo.save_user(User(chat_id=req.chat_id, enabled=True))

        if not user.enabled:
            return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.USER_DISABLED)

        user_state = self.user_state_use_case.get_user_state(user.id)

        if user_state.state.module == Module.PLACES:
            return self.handle_places(user, req.massage, req.longitude, req.latitude)

        elif user_state.state.module == Module.ABOUT_BOT:
            self.handle_about_bot()

        elif user_state.state.module == Module.DECISION_TREE:
            return self.handle_decision_tree(user, user_state.state.category, user_state.state.step, req.massage)

        elif user_state.state.module == Module.INIT:
            return self.handle_init(user, req.massage)




        return ReceiveMassageResponse(chat_id=req.chat_id, status=Status.OK)

    def handle_places(self, user, message, longitude=None, latitude=None):
        mod = self.user_state_use_case.get_user_state(user.id).state.module
        if mod == Module.INIT:
            titles = [self.pharmacy_message, self.hospital_message]
            state = self.user_state_use_case.set_user_state(
                UpdateUserStateRequest(user_id=user.id, module=Module.PLACES, category='', step=''))
            if state is None:
                return ReceiveMassageResponse(chat_id=user.chat_id, status=Status.ERROR)
            return ReceiveMassageResponse(chat_id=user.chat_id, status=Status.OK, titles=titles, module=mod)

        if mod == Module.PLACES:
            if longitude == '' or latitude == '':
                return ReceiveMassageResponse(chat_id=user.chat_id, status=Status.ERROR)
            gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API_KEY'))

            location = (latitude, longitude)
            place_type = None
            if message == self.pharmacy_message:
                place_type = 'pharmacy'
            elif place_type == self.hospital_message:
                place_type = 'hospital'
            else:
                ReceiveMassageResponse(chat_id=user.chat_id, status=Status.ERROR)

            places_result = gmaps.places_nearby(location=location, type=place_type, language='uk',
                                                open_now=True, rank_by='distance', keyword=message)
            places = []

            for place_result in places_result['results'][:5]:
                place_location = place_result['geometry']['location']
                places.append(Place(place_name=place_result['name'], place_address=place_result['vicinity'],
                                    longitude=place_location['lng'], latitude=place_location['lat']))

            return ReceiveMassageResponse(chat_id=user.chat_id, status=Status.OK, module=mod, places=places)

    def handle_about_bot(self):
        pass

    def handle_decision_tree(self, user, category, step, message):
        dt_nodes_resp = self.decision_tree_use_case.find_nodes_in_decision_tree(category, step, message)
        if dt_nodes_resp is None or dt_nodes_resp.status == Status.ERROR:
            return ReceiveMassageResponse(chat_id=user.chat_id, status=Status.ERROR)

        state = self.user_state_use_case.set_user_state(UpdateUserStateRequest(user_id=user.id, module=Module.DECISION_TREE, category=category, step=dt_nodes_resp.step))
        if state is None:
            return ReceiveMassageResponse(chat_id=user.chat_id, status=Status.ERROR)

        titles = self.get_titles(dt_nodes_resp.nodes)
        mod = self.user_state_use_case.get_user_state(user.id).state.module
        return ReceiveMassageResponse(chat_id=user.chat_id, status=Status.OK, instruction=dt_nodes_resp.instruction, image=dt_nodes_resp.image, titles=titles, module=mod)

    def handle_init(self, user, message):
        categories = self.decision_tree_use_case.get_categories()
        if message in categories:
            return self.handle_decision_tree(user, message, step='', message=None)

        if message == self.places_message:
            return self.handle_places(user, message)

        if message == self.about_message:
            self.handle_about_bot()
        return ReceiveMassageResponse(chat_id=user.chat_id, status=Status.ERROR)

    def get_titles(self, nodes: [DecisionTreeNode]) -> [str]:
        titles = []
        if nodes is None:
            return None
        for node in nodes:
            titles.append(node.title)
        return titles


class UserStateUseCaseFactory(object):
    @staticmethod
    def get() -> IUserStateUseCase:
        return UserStateUseCase(UserStateRepoFactory.get())

class UserStateUseCase(IUserStateUseCase):
    def __init__(self, repo: IUserStateRepository):
        self.repo = repo

    def init_user_state(self, user_id: int) -> InitUserStateResponse:
        state = self.repo.get_by_user_id(user_id=user_id)

        if state is None:
            state = UserState(user_id=user_id, module=Module.INIT)
        else:
            state.module = Module.INIT
            state.step = ''
            state.category = ''
        state = self.repo.save_user_state(state)

        if state is None:
            return InitUserStateResponse(status=Status.ERROR)

        return InitUserStateResponse(status=Status.OK)


    def set_user_state(self, req: UpdateUserStateRequest) -> UpdateUserStateResponse:
        state = self.repo.get_by_user_id(user_id=req.user_id)
        if state is None:
            return UpdateUserStateResponse(status=Status.ERROR)

        state.module = req.module
        state.category = req.category
        state.step = req.step

        state = self.repo.save_user_state(state)

        if state is None:
            return UpdateUserStateResponse(status=Status.ERROR)

        return UpdateUserStateResponse(status=Status.OK)

    def get_user_state(self, user_id: int) -> GetUserStateResponse:
        state = self.repo.get_by_user_id(user_id=user_id)
        if state is None:
            return GetUserStateResponse(status=Status.ERROR)

        return GetUserStateResponse(status=Status.OK, state=state)

