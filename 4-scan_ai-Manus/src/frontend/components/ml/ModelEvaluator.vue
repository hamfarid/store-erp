              <div class="form-group">
                <label for="evaluation-model">النموذج</label>
                <select 
                  id="evaluation-model"
                  v-model="evaluationConfig.modelId"
                >
                  <option v-for="model in models" :key="model.id" :value="model.id">
                    {{ model.name }}
                  </option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="evaluation-dataset">مجموعة البيانات</label>
                <select 
                  id="evaluation-dataset"
                  v-model="evaluationConfig.datasetId"
                >
                  <option v-for="dataset in datasets" :key="dataset.id" :value="dataset.id">
                    {{ dataset.name }}
                  </option>
                </select>
              </div>
              
              <div class="form-group">
                <label for="evaluation-metrics">مقاييس التقييم</label>
                <div class="metrics-grid">
                  <label class="metric-option" for="metric-accuracy">
                    <input 
                      id="metric-accuracy"
                      type="checkbox" 
                      v-model="evaluationConfig.metrics.accuracy"
                    />
                    <span>الدقة (Accuracy)</span>
                  </label>
                  
                  <label class="metric-option" for="metric-precision">
                    <input 
                      id="metric-precision"
                      type="checkbox" 
                      v-model="evaluationConfig.metrics.precision"
                    />
                    <span>الدقة (Precision)</span>
                  </label>
                  
                  <label class="metric-option" for="metric-recall">
                    <input 
                      id="metric-recall"
                      type="checkbox" 
                      v-model="evaluationConfig.metrics.recall"
                    />
                    <span>الاسترجاع (Recall)</span>
                  </label>
                  
                  <label class="metric-option" for="metric-f1">
                    <input 
                      id="metric-f1"
                      type="checkbox" 
                      v-model="evaluationConfig.metrics.f1"
                    />
                    <span>مقياس F1</span>
                  </label>
                  
                  <label class="metric-option" for="metric-confusion">
                    <input 
                      id="metric-confusion"
                      type="checkbox" 
                      v-model="evaluationConfig.metrics.confusionMatrix"
                    />
                    <span>مصفوفة الارتباك</span>
                  </label>
                </div>
              </div>
              
              <div class="form-group">
                <label for="evaluation-batch-size">حجم الدفعة</label>
                <input 
                  id="evaluation-batch-size"
                  type="number" 
                  v-model="evaluationConfig.batchSize" 
                  min="1"
                  max="128"
                />
              </div>
              
              <div class="form-group">
                <label for="evaluation-threshold">عتبة التصنيف</label>
                <input 
                  id="evaluation-threshold"
                  type="number" 
                  v-model="evaluationConfig.threshold" 
                  min="0"
                  max="1"
                  step="0.01"
                />
              </div> 