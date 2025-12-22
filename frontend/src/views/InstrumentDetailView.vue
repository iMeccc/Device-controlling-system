<template>
  <div class="detail-container">
    <el-page-header @back="goBack" content="仪器详情与预约" />
    <el-divider />

    <!-- FIX 3: Instrument details section is now correctly included -->
    <el-card v-if="instrument" class="instrument-card" v-loading="loading.details">
      <template #header>
        <div class="card-header">
          <span>{{ instrument.name }} - {{ instrument.model }}</span>
        </div>
      </template>
      <p><strong>位置:</strong> {{ instrument.location }}</p>
      <p><strong>描述:</strong> {{ instrument.description }}</p>
      <p><strong>状态:</strong> {{ instrument.status }}</p>
    </el-card>

    <el-divider />
    <h2>预约日历</h2>
    <el-calendar v-model="selectedDate">
      <template #date-cell="{ data }">
        <div class="date-cell" @click="handleDateClick(data)">
          <span class="date-number">{{ data.day.split('-').slice(2).join('') }}</span>
          <!-- FIX 1 & 2: Dot indicator for reservations -->
          <div v-if="getReservationsForDate(data.day).length > 0" class="dot"></div>
        </div>
      </template>
    </el-calendar>
  </div>

  <!-- Dialog for creating a new reservation -->
  <el-dialog v-model="dialogVisible" :title="`预约 - ${selectedDay}`" width="60%">
    <div class="dialog-content">
      <div class="existing-reservations">
        <h4>当天已有预约</h4>
        <el-timeline v-if="todaysReservations.length > 0">
          <el-timeline-item
            v-for="res in todaysReservations"
            :key="res.id"
            :timestamp="`${formatTime(res.start_time)} - ${formatTime(res.end_time)}`"
          >
            <span>已预约</span>
          </el-timeline-item>
        </el-timeline>
        <el-empty v-else description="当天暂无预约" />
      </div>

      <div class="new-reservation">
        <h4>选择预约时间段</h4>
        <el-select v-model="newReservation.startTime" placeholder="开始时间" style="width: 100%;">
          <el-option
            v-for="slot in availableTimeSlots"
            :key="slot.time"
            :label="slot.time"
            :value="slot.time"
            :disabled="slot.disabled"
          />
        </el-select>
        <el-select v-model="newReservation.endTime" placeholder="结束时间" style="width: 100%; margin-top: 10px;">
          <el-option
            v-for="slot in availableTimeSlots.slice(1)"
            :key="slot.time"
            :label="slot.time"
            :value="slot.time"
            :disabled="!isEndTimeValid(slot.time)"
          />
        </el-select>
      </div>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReservation">提交预约</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { getInstrumentById, getReservationsByInstrument, createReservation } from '@/services/api';

const route = useRoute();
const router = useRouter();
const instrumentId = ref(null);
const instrument = ref(null);
const reservations = ref([]);
const loading = reactive({ details: true, calendar: true });
const selectedDate = ref(new Date());
const dialogVisible = ref(false);
const selectedDay = ref('');
const newReservation = reactive({ startTime: null, endTime: null });

const todaysReservations = computed(() => {
  if (!selectedDay.value) return [];
  return getReservationsForDate(selectedDay.value).sort((a, b) => new Date(a.start_time) - new Date(b.start_time));
});

const timeSlots = Array.from({ length: 48 }, (_, i) => {
  const hour = Math.floor(i / 2).toString().padStart(2, '0');
  const minute = (i % 2 === 0) ? '00' : '30';
  return `${hour}:${minute}`;
});

const availableTimeSlots = computed(() => {
  if (!selectedDay.value) return [];
  const now = new Date();
  const thirtyMinutesFromNow = new Date(now.getTime() + 30 * 60 * 1000);

  return timeSlots.map(slot => {
    const [hour, minute] = slot.split(':');
    const slotStartDateTime = new Date(selectedDay.value);
    slotStartDateTime.setHours(hour, minute, 0, 0);
    const slotEndDateTime = new Date(slotStartDateTime.getTime() + 30 * 60 * 1000);

    const isPast = slotStartDateTime < thirtyMinutesFromNow && isToday(slotStartDateTime);

    const isBooked = todaysReservations.value.some(res => {
      const resStart = new Date(res.start_time);
      const resEnd = new Date(res.end_time);
      return slotStartDateTime < resEnd && slotEndDateTime > resStart;
    });

    return { time: slot, disabled: isPast || isBooked };
  });
});

const isEndTimeValid = (endTime) => {
  if (!newReservation.startTime) return false;
  if (endTime <= newReservation.startTime) return false;
  
  const startIndex = timeSlots.indexOf(newReservation.startTime);
  const endIndex = timeSlots.indexOf(endTime);
  for (let i = startIndex; i < endIndex; i++) {
    const slot = availableTimeSlots.value[i];
    if (slot && slot.disabled) {
      return false;
    }
  }
  return true;
};

onMounted(async () => {
  instrumentId.value = route.params.id;
  if (instrumentId.value) {
    await fetchData();
  }
});

const fetchData = async () => {
  loading.details = true;
  loading.calendar = true;
  try {
    const [instData, resData] = await Promise.all([
      getInstrumentById(instrumentId.value),
      getReservationsByInstrument(instrumentId.value)
    ]);
    instrument.value = instData;
    reservations.value = resData;
  } catch (error) {
    console.error("Fetch data failed:", error);
    ElMessage.error('获取数据失败，请检查网络或联系管理员。');
  } finally {
    loading.details = false;
    loading.calendar = false;
  }
};

const goBack = () => {
  router.push('/dashboard');
};

const handleDateClick = (data) => {
  const clickedDate = new Date(data.day);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  if (data.type === 'current-month' && clickedDate >= today) {
    selectedDay.value = data.day;
    newReservation.startTime = null;
    newReservation.endTime = null;
    dialogVisible.value = true;
  } else if (clickedDate < today) {
    ElMessage.info('不能为过去的日期创建预约。');
  }
};

const submitReservation = async () => {
  if (!newReservation.startTime || !newReservation.endTime) {
    ElMessage.error('请选择完整的开始和结束时间。');
    return;
  }

  const startDateTime = new Date(`${selectedDay.value}T${newReservation.startTime}:00`);
  const endDateTime = new Date(`${selectedDay.value}T${newReservation.endTime}:00`);

  const reservationData = {
    instrument_id: parseInt(instrumentId.value),
    start_time: startDateTime.toISOString(),
    end_time: endDateTime.toISOString(),
  };

  try {
    await createReservation(reservationData);
    ElMessage.success('预约成功！');
    dialogVisible.value = false;
    await fetchData();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '预约失败，时间段可能已被占用。');
  }
};

const getReservationsForDate = (date) => {
  return reservations.value.filter(res => res.start_time && res.start_time.startsWith(date));
};

const formatTime = (isoString) => {
  if (!isoString) return '';
  return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const isToday = (someDate) => {
  const today = new Date();
  return someDate.getDate() === today.getDate() &&
         someDate.getMonth() === today.getMonth() &&
         someDate.getFullYear() === today.getFullYear();
};
</script>

<style scoped>
.dialog-content { display: flex; gap: 20px; }
.existing-reservations, .new-reservation { flex: 1; }
.dot {
  width: 8px;
  height: 8px;
  background-color: #67c23a;
  border-radius: 50%;
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
}
.date-cell {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 4px;
  cursor: pointer;
}
.date-number {
  font-weight: bold;
}
</style>