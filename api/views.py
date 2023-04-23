from rest_framework.views import APIView

from utils.utils_views import CustomResponse
from .data import get_question_details, save_json, generate_ticket, mark_attendance,load_attendance_data
from rest_framework.exceptions import ValidationError

class CollectFormDataAPI(APIView):
    def get(self, request):
        questions = get_question_details()
        return CustomResponse(response=questions).get_success_response()

    def post(self, request):
        full_name = request.data.get('fullName')
        email = request.data.get('email')
        job_title = request.data.get('jobTitle')
        interests = request.data.get('interests')
        event_source = request.data.get('eventSource')
        additional_comments = request.data.get("additionalComments")

        if full_name is None:
            return CustomResponse(general_message="FullName is required").get_success_response()

        if email is None:
            return CustomResponse(general_message="Email is required").get_success_response()

        save_json(full_name, email, job_title, interests, event_source, additional_comments)

        return CustomResponse(general_message="daata").get_success_response()


class TicketGeneration(APIView):

    def get(self, request):
        return CustomResponse(response=generate_ticket()).get_success_response()


class AttendanceAPI(APIView):
    def get(self, request):
        return CustomResponse(response=load_attendance_data()).get_success_response()

    def post(self, request):
        email = request.data.get("email")
        try:
            if not mark_attendance(email):
                return CustomResponse(general_message="Attendance Exists").get_failure_response()
            return CustomResponse(general_message="Attendance Marked").get_success_response()
        except ValidationError as e:
            return CustomResponse(general_message="Ticket Not Exists").get_failure_response()
