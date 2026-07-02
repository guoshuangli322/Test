from django.http import JsonResponse
from apps.dorm.models import Room, Bed

def get_rooms_by_building(request):
    """AJAX: 根据楼栋获取房间列表"""
    building_id = request.GET.get('building_id')
    rooms = Room.objects.filter(building_id=building_id, is_active=True)
    data = [{'id': r.id, 'text': f'{r.building.code}-{r.room_number}(空闲{r.available_bed_count()}/{r.bed_count})'} for r in rooms]
    return JsonResponse(data, safe=False)

def get_beds_by_room(request):
    """AJAX: 根据房间获取空闲床位"""
    room_id = request.GET.get('room_id')
    beds = Bed.objects.filter(room_id=room_id, status='空闲')
    data = [{'id': b.id, 'text': b.bed_number} for b in beds]
    return JsonResponse(data, safe=False)
