<!-- File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/settings/CompanyManagement.vue -->
<template>
  <div class="company-management">
    <v-card>
      <v-card-title>
        <span>Company Management</span>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>

      <v-data-table
        :headers="headers"
        :items="companies"
        :search="search"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            class="mr-2"
            @click="editItem(item)"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            small
            class="mr-2"
            @click="toggleStatus(item)"
          >
            mdi-toggle-switch
          </v-icon>
          <v-icon
            small
            @click="deleteItem(item)"
          >
            mdi-delete
          </v-icon>
        </template>

        <template v-slot:item.active="{ item }">
          <v-chip
            :color="item.active ? 'success' : 'error'"
            small
          >
            {{ item.active ? 'Active' : 'Inactive' }}
          </v-chip>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="editedItem.name"
                  label="Company Name"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="editedItem.country"
                  label="Country"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="editedItem.currency"
                  label="Currency"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="editedItem.taxId"
                  label="Tax ID"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'CompanyManagement',
  
  setup() {
    const store = useStore()
    const search = ref('')
    const dialog = ref(false)
    const loading = ref(false)
    const companies = ref([])
    const headers = [
      { text: 'Name', value: 'name' },
      { text: 'Country', value: 'country' },
      { text: 'Currency', value: 'currency' },
      { text: 'Tax ID', value: 'taxId' },
      { text: 'Status', value: 'active' },
      { text: 'Actions', value: 'actions', sortable: false }
    ]
    const editedIndex = ref(-1)
    const editedItem = ref({
      name: '',
      country: '',
      currency: '',
      taxId: '',
      active: true
    })
    const defaultItem = {
      name: '',
      country: '',
      currency: '',
      taxId: '',
      active: true
    }

    const formTitle = computed(() => {
      return editedIndex.value === -1 ? 'New Company' : 'Edit Company'
    })

    const initialize = async () => {
      loading.value = true
      try {
        const response = await store.dispatch('companies/fetchCompanies')
        companies.value = response.data
      } catch (error) {
        ElMessage.error('Failed to load companies')
      } finally {
        loading.value = false
      }
    }

    const editItem = (item) => {
      editedIndex.value = companies.value.indexOf(item)
      editedItem.value = Object.assign({}, item)
      dialog.value = true
    }

    const deleteItem = async (item) => {
      try {
        await store.dispatch('companies/deleteCompany', item.id)
        companies.value = companies.value.filter(company => company.id !== item.id)
        ElMessage.success('Company deleted successfully')
      } catch (error) {
        ElMessage.error('Failed to delete company')
      }
    }

    const toggleStatus = async (item) => {
      try {
        await store.dispatch('companies/updateCompany', {
          ...item,
          active: !item.active
        })
        const index = companies.value.findIndex(company => company.id === item.id)
        companies.value[index].active = !item.active
        ElMessage.success('Company status updated successfully')
      } catch (error) {
        ElMessage.error('Failed to update company status')
      }
    }

    const close = () => {
      dialog.value = false
      editedItem.value = Object.assign({}, defaultItem)
      editedIndex.value = -1
    }

    const save = async () => {
      try {
        if (editedIndex.value > -1) {
          await store.dispatch('companies/updateCompany', editedItem.value)
          Object.assign(companies.value[editedIndex.value], editedItem.value)
        } else {
          const response = await store.dispatch('companies/createCompany', editedItem.value)
          companies.value.push(response.data)
        }
        ElMessage.success('Company saved successfully')
        close()
      } catch (error) {
        ElMessage.error('Failed to save company')
      }
    }

    onMounted(() => {
      initialize()
    })

    return {
      search,
      dialog,
      loading,
      companies,
      headers,
      editedIndex,
      editedItem,
      formTitle,
      editItem,
      deleteItem,
      toggleStatus,
      close,
      save
    }
  }
}
</script>

<style scoped>
.company-management {
  padding: 20px;
}
</style>
